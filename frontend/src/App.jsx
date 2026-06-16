import React, { useState, useEffect, useRef } from 'react'
import ResultsPanel from './components/ResultsPanel'

function App() {
  const [image, setImage] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const [logs, setLogs] = useState([
    { time: 'T-MINUS 00:00:00', text: 'Diagnostic scan complete. All systems nominal.', type: 'normal' },
    { time: 'T-MINUS 00:02:14', text: 'Neural sync established with core node.', type: 'normal' },
  ])
  const [inputValue, setInputValue] = useState('')
  const fileInputRef = useRef(null)
  const logsEndRef = useRef(null)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const addLog = (text, type = 'normal') => {
    const now = new Date()
    const timeStr = `T-MINUS ${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}:${String(now.getMilliseconds()).padStart(3, '0').substring(0, 2)}`
    setLogs(prev => [...prev, { time: timeStr, text, type }])
  }

  // Auto-scroll logs
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  const handleImageUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    setImage({
      file,
      preview: URL.createObjectURL(file)
    })
    
    setLoading(true)
    setError(null)
    setResults(null)
    addLog(`Initiating neural scan on specimen: ${file.name}...`, 'normal')

    const formData = new FormData()
    formData.append('image', file) // IMPORTANT: Must be 'image' for backend

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`Neural Link Severed: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      setResults(data)
      addLog(`Scan complete. Target identified: ${data.disease_info?.disease_name || 'Unknown'}`, 'success')
      
      if (data.weighted_confidence < 0.5) {
        addLog(`Warning: Core Resonance below nominal threshold (${(data.weighted_confidence * 100).toFixed(1)}%).`, 'warning')
      }
      
    } catch (err) {
      setError(err.message || 'System Failure. Unable to communicate with the Neural Engine.')
      addLog(`ERR: ${err.message}`, 'warning')
    } finally {
      setLoading(false)
    }
  }

  const handleSyncSystem = async () => {
    addLog('Initiating System Sync...', 'normal')
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      if (response.ok) {
        const data = await response.json()
        addLog(`Sync Successful. Inference Engine: ${data.inference_engine}. Sensors: ${data.sensors}.`, 'success')
      } else {
        addLog(`Sync Failed: Node unresponsive.`, 'warning')
      }
    } catch (e) {
      addLog(`Critical Sync Failure: ${e.message}`, 'warning')
    }
  }

  const handleSidebarNav = (sector) => {
    addLog(`Redirecting neural pathways to sector: ${sector}...`, 'normal')
  }

  const handleInputSubmit = (e) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      addLog(`> ${inputValue}`, 'normal')
      
      const cmd = inputValue.trim().toLowerCase()
      if (cmd === 'ping') {
        setTimeout(() => addLog('PONG', 'success'), 500)
      } else if (cmd === 'clear') {
        setLogs([])
      } else {
        setTimeout(() => addLog(`Command not recognized: ${inputValue}`, 'warning'), 500)
      }
      
      setInputValue('')
    }
  }

  const aiConfidence = results?.top_prediction?.confidence || 0
  const energyOutputPercent = loading ? '100%' : `${(aiConfidence * 100).toFixed(1)}%`

  return (
    <div className="bg-background text-on-background min-h-screen overflow-hidden selection:bg-moss-green selection:text-white">
      {/* Faux Background */}
      <div className="fixed inset-0 z-[-2] bg-ambient">
        <img alt="Bioluminescent leaf" className="w-full h-full object-cover opacity-40 mix-blend-screen" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDIv4Ss3zV5mBlqWy2uklqZuul4p2hhCyRmGRHtaManvxIurdFbT8VegNLsGRZG7KH8mPWAqspl_-8UujeiJefzZmY7RGXtMdcTnyzxUoaIL4Bc0pLGvyjbqop9mAhU6RhFsafcl8a-6gXWuAXv6RMPxDFxFkFxrPXdWAfAUAA8hy92m5yLh1TlrAkcO2lLNZ7rwGifjUuxEu-RMYVrYq0QwJt29U4atJLQWreybRj9UvPtjjPQaOCUYUA-JhmFiywfA366y5nET0Q"/>
      </div>

      {/* TopNavBar */}
      <nav className="fixed top-0 w-full z-50 flex justify-between items-center px-margin py-4 bg-transparent border-b border-sovereign-gold/20 backdrop-blur-md transition-all duration-300 ease-out hidden md:flex">
        <div className="font-headline-sm text-headline-sm tracking-widest text-sky-blue drop-shadow-[0_0_10px_rgba(135,206,235,0.5)] uppercase">
          BIO-SYNTHESIS HUD
        </div>
        <div className="flex gap-8">
          <a className="font-label-caps text-label-caps text-moss-green border-b border-moss-green pb-1 uppercase" href="#">Neural Link</a>
          <a className="font-label-caps text-label-caps text-on-surface-variant/80 hover:text-moss-green hover:drop-shadow-[0_0_8px_rgba(74,103,65,0.8)] uppercase" href="#">Flora Metrics</a>
          <a className="font-label-caps text-label-caps text-on-surface-variant/80 hover:text-moss-green hover:drop-shadow-[0_0_8px_rgba(74,103,65,0.8)] uppercase" href="#">Archive</a>
          <a className="font-label-caps text-label-caps text-on-surface-variant/80 hover:text-moss-green hover:drop-shadow-[0_0_8px_rgba(74,103,65,0.8)] uppercase" href="#">Control</a>
        </div>
        <div className="flex gap-4 text-sky-blue">
          <span className="material-symbols-outlined cursor-pointer hover:drop-shadow-[0_0_8px_rgba(135,206,235,0.8)]">settings</span>
          <span className="material-symbols-outlined cursor-pointer hover:drop-shadow-[0_0_8px_rgba(135,206,235,0.8)]">notifications</span>
        </div>
      </nav>

      {/* SideNavBar */}
      <aside className="fixed left-0 top-1/2 -translate-y-1/2 z-40 flex flex-col py-panel-padding bg-primary-container/40 h-[819px] w-64 rounded-r-xl my-auto border-r border-sovereign-gold/40 backdrop-blur-2xl shadow-[0_0_20px_rgba(0,0,0,0.5)] hidden md:flex justify-between">
        <div className="px-6 pb-8 border-b border-sovereign-gold/20 mb-4">
          <div className="w-16 h-16 rounded-full border border-moss-green p-1 mb-4 pulse-glow">
            <img alt="Bio-Metric Pulse" className="w-full h-full rounded-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCGLDLJHCjOdCTgYtg-Agwr9HtHkHfybDJ28SS7n0xdXfcnz2onvPwnrP41B0EDTWmVUJ3MgUPwO1I6EeY-YV2FQ2rAe1GBQjPT6nq-9gRaZ1j1rlkEhia5ERgeICca7fe6yRPRW2shU41aAQrF9_ixpihHXOljr0qWT7Umqfb8kKzyU6LMMNct-8Ustb9BX9bslgapjWc3HeQeDLlegsiV-D9RSVkq_oeRypZGXju7CLpUjBvozEW1Pbly_Ki70nzVek6DK-ETwIM"/>
          </div>
          <div className="font-label-caps text-label-caps text-sovereign-gold uppercase tracking-widest">NODE 07-X</div>
          <div className="font-technical-data text-technical-data text-sovereign-gold/60 mt-1">LAT: 40.7128 N</div>
        </div>
        <nav className="flex flex-col gap-2 flex-grow">
          <button onClick={() => handleSidebarNav('Atmosphere')} className="flex items-center gap-4 text-on-surface-variant/60 hover:text-on-surface hover:bg-primary-container/60 pl-4 py-3 font-technical-data text-technical-data uppercase transition-colors text-left">
            <span className="material-symbols-outlined">air</span> Atmosphere
          </button>
          <button onClick={() => handleSidebarNav('Hydration')} className="flex items-center gap-4 text-on-surface-variant/60 hover:text-on-surface hover:bg-primary-container/60 pl-4 py-3 font-technical-data text-technical-data uppercase transition-colors text-left">
            <span className="material-symbols-outlined">water_drop</span> Hydration
          </button>
          <button onClick={() => handleSidebarNav('Core Temp')} className="flex items-center gap-4 text-on-surface-variant/60 hover:text-on-surface hover:bg-primary-container/60 pl-4 py-3 font-technical-data text-technical-data uppercase transition-colors text-left">
            <span className="material-symbols-outlined">thermostat</span> Core Temp
          </button>
          <button onClick={() => handleSidebarNav('Neural Sync')} className="flex items-center gap-4 bg-moss-green/10 text-moss-green border-l-2 border-moss-green pl-4 py-3 font-technical-data text-technical-data transition-transform duration-200 scale-95 uppercase text-left">
            <span className="material-symbols-outlined">psychology</span> Neural Sync
          </button>
        </nav>
        <div className="px-6 mt-auto pt-8">
          <button onClick={handleSyncSystem} className="w-full py-3 bg-primary-container text-moss-green border border-moss-green font-label-caps text-label-caps uppercase tracking-widest hover:bg-moss-green/10 pulse-glow transition-all">
            Sync System
          </button>
        </div>
      </aside>

      {/* Main Content Canvas */}
      <main className="ml-0 md:ml-64 pt-24 px-margin pb-24 h-screen overflow-y-auto z-10 relative">
        <div className="grid grid-cols-12 gap-gutter h-full">
          
          {/* Center Display */}
          <div className="col-span-12 lg:col-span-8 flex flex-col gap-element-gap">
            <ResultsPanel 
              image={image} 
              results={results} 
              loading={loading} 
              error={error} 
              onInitializeScan={() => fileInputRef.current?.click()}
            />
            
            {/* Secondary Data Panels */}
            <div className="grid grid-cols-2 gap-element-gap h-48">
              <div className="glass-panel rounded-lg p-6 relative">
                <div className="font-label-caps text-label-caps text-sovereign-gold mb-4 uppercase">Energy Output</div>
                <div className="h-2 w-full bg-sovereign-gold/20 rounded-full overflow-hidden mt-8">
                  <div 
                    className="h-full bg-moss-green shadow-[0_0_10px_#4A6741] transition-all duration-1000 ease-out" 
                    style={{ width: energyOutputPercent }}
                  ></div>
                </div>
                <div className="flex justify-between mt-2 font-technical-data text-technical-data text-on-surface-variant/80">
                  <span>0.0</span>
                  <span>75.0</span>
                  <span>100.0</span>
                </div>
              </div>
              <div className="glass-panel rounded-lg p-6 relative flex items-center justify-center">
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  className="hidden" 
                  accept="image/*" 
                  onChange={handleImageUpload}
                />
                <button 
                  onClick={() => fileInputRef.current?.click()}
                  disabled={loading}
                  className="px-8 py-4 bg-primary-container border border-sovereign-gold text-sovereign-gold font-label-caps text-label-caps uppercase tracking-widest hover:border-moss-green hover:text-moss-green transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Scanning...' : 'Initialize Scan'}
                </button>
              </div>
            </div>
          </div>

          {/* Right Sidebar Panel */}
          <div className="col-span-12 lg:col-span-4 glass-panel rounded-lg p-panel-padding flex flex-col max-h-full">
            <div className="font-label-caps text-label-caps text-sovereign-gold mb-6 uppercase border-b border-sovereign-gold/20 pb-2">Log Stream</div>
            <div className="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar">
              {logs.map((log, i) => (
                <div key={i} className={`border-l-2 pl-4 ${
                  log.type === 'warning' ? 'border-error bg-error-container/20 p-2 rounded-r' : 
                  log.type === 'success' ? 'border-moss-green' : 
                  'border-sky-blue'
                }`}>
                  <div className={`font-technical-data text-technical-data text-xs mb-1 ${
                    log.type === 'warning' ? 'text-error' : 'text-on-surface-variant/80'
                  }`}>{log.time}</div>
                  <div className={`font-body-md text-body-md ${
                    log.type === 'warning' ? 'text-error' : 'text-on-surface'
                  }`}>{log.text}</div>
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
            <div className="mt-6 pt-6 border-t border-sovereign-gold/20">
              <div className="font-label-caps text-label-caps text-sovereign-gold mb-2 uppercase">Input Directive</div>
              <div className="relative">
                <input 
                  className="w-full bg-transparent border-0 border-b border-sovereign-gold/40 focus:border-moss-green focus:ring-0 text-moss-green font-technical-data px-0 py-2 placeholder:text-on-surface-variant/50 outline-none" 
                  placeholder="> AWAITING COMMAND..." 
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleInputSubmit}
                />
              </div>
            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="fixed bottom-0 w-full z-50 flex justify-between items-center px-margin py-2 bg-transparent border-t border-sovereign-gold/10 cursor-pointer hidden md:flex">
        <div className="font-technical-data text-technical-data uppercase text-sovereign-gold/40">
          © 2142 NEURALIS INDUSTRIES. ALL SYSTEMS NOMINAL.
        </div>
        <div className="flex gap-6 font-technical-data text-technical-data uppercase text-sovereign-gold/40">
          <a className="hover:text-sky-blue transition-colors" href="#">Privacy Protocol</a>
          <a className="hover:text-sky-blue transition-colors" href="#">Terms of Service</a>
        </div>
      </footer>
    </div>
  )
}

export default App
