import React from 'react'

export default function ResultsPanel({ image, results, loading, error, onInitializeScan }) {
  // Data Mapping
  const o2Saturation = results?.sensor_readings?.humidity 
    ? `${results.sensor_readings.humidity.toFixed(1)}%` 
    : "98.4%";
  
  const fluxDensity = results?.sensor_readings?.soil_moisture 
    ? `+${(results.sensor_readings.soil_moisture / 10).toFixed(4)}` 
    : "+4.6076";
  
  const coreResonance = results?.weighted_confidence;
  const isResonanceLow = results && coreResonance < 0.5;
  const resonanceDisplay = results 
    ? `${(coreResonance * 100).toFixed(1)}%` 
    : "NOMINAL";

  return (
    <section className="col-span-12 lg:col-span-7 glass-panel flex flex-col h-full rounded-lg shadow-2xl overflow-hidden relative">
      <div className="p-8 flex flex-col h-full">
        <header className="flex justify-between items-center mb-6">
          <h1 className="font-h1 text-h1 text-on-surface gothic-glow-gold uppercase">
            {loading ? 'Scanning...' : (error ? 'System Error' : 'Synthesis Active')}
          </h1>
          <span className="font-terminal-data text-terminal-data text-secondary px-3 py-1 bg-secondary/10 rounded border border-secondary/20 gothic-glow-cyan">
            LIVE_FEED
          </span>
        </header>

        {/* HUD Wrapper */}
        <div className="h-[409px] w-full border border-primary/30 rounded-lg relative flex items-center justify-center bg-surface-container-lowest/50 mb-8 overflow-hidden group">
          
          {/* Reticle */}
          {!image && !results && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-50">
              <div className="w-64 h-64 border border-secondary/20 rounded-full flex items-center justify-center relative animate-spin-slow">
                <div className="w-px h-full bg-secondary/30 absolute"></div>
                <div className="h-px w-full bg-secondary/30 absolute"></div>
                <div className="absolute inset-0 border border-secondary/40 rounded-full scale-75 border-dashed"></div>
              </div>
            </div>
          )}

          {/* HUD Metadata */}
          <div className="absolute top-4 left-4 font-terminal-data text-terminal-data text-secondary/70 z-20">
            [X: 45.992, Y: -12.004, Z: 0.001]
          </div>
          <div className="absolute bottom-4 right-4 font-terminal-data text-terminal-data text-secondary/70 z-20">
            SEQ_ID: 994-A7
          </div>

          <div className="w-full h-full bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-secondary/5 to-transparent relative z-10 flex items-center justify-center">
            {/* Specimen / GradCAM Rendering */}
            {results?.gradcam_image ? (
              <img 
                src={results.gradcam_image}
                alt="Analyzed Specimen" 
                className="w-full h-full object-contain"
              />
            ) : image ? (
              <img 
                src={image.preview} 
                alt="Uploaded Specimen" 
                className={`w-full h-full object-contain ${loading ? 'grayscale opacity-50 pulse-glow' : ''}`}
              />
            ) : null}
          </div>
        </div>

        {/* Metric Grid */}
        <div className="grid grid-cols-3 gap-6 mb-8 flex-grow">
          <div className="border border-white/5 bg-surface/40 p-4 rounded-lg flex flex-col justify-between">
            <span className="font-label-caps text-label-caps text-on-surface-variant">O2 SATURATION</span>
            <div className="font-terminal-data text-terminal-data text-xl text-secondary mt-2 gothic-glow-cyan">{o2Saturation}</div>
            <div className="h-1 w-full bg-surface-variant mt-4 rounded-full overflow-hidden">
              <div className="h-full bg-secondary w-[99%]"></div>
            </div>
          </div>
          
          <div className="border border-white/5 bg-surface/40 p-4 rounded-lg flex flex-col justify-between">
            <span className="font-label-caps text-label-caps text-on-surface-variant">FLUX DENSITY</span>
            <div className="font-terminal-data text-terminal-data text-xl text-primary mt-2 gothic-glow-gold">{fluxDensity}</div>
            <div className="h-1 w-full bg-surface-variant mt-4 rounded-full overflow-hidden flex justify-center items-center">
              <div className="h-full bg-primary w-[46%] mx-auto"></div>
            </div>
          </div>
          
          <div className={`border p-4 rounded-lg flex flex-col justify-between relative overflow-hidden ${
            isResonanceLow 
              ? 'border-error/20 bg-error/5 shadow-[0_0_15px_rgba(255,42,42,0.1)]' 
              : 'border-white/5 bg-surface/40'
          }`}>
            {isResonanceLow && <div className="absolute inset-0 bg-error/10 animate-pulse"></div>}
            <span className={`font-label-caps text-label-caps relative z-10 ${isResonanceLow ? 'text-error' : 'text-on-surface-variant'}`}>
              CORE RESONANCE
            </span>
            <div className={`font-terminal-data text-terminal-data text-xl mt-2 relative z-10 flex items-center gap-2 ${
              isResonanceLow ? 'text-[#FF2A2A] gothic-glow-crimson' : 'text-primary gothic-glow-gold'
            }`}>
              {isResonanceLow && <span className="material-symbols-outlined text-sm">warning</span>}
              {isResonanceLow ? 'ERR: LOW' : resonanceDisplay}
            </div>
            <div className={`h-1 w-full mt-4 rounded-full overflow-hidden relative z-10 ${isResonanceLow ? 'bg-error/20' : 'bg-surface-variant'}`}>
              <div className={`h-full ${isResonanceLow ? 'bg-[#FF2A2A] w-[12%]' : 'bg-primary w-[98%]'}`}></div>
            </div>
          </div>
        </div>

        <button 
          onClick={onInitializeScan}
          disabled={loading}
          className="w-full py-4 border-t-2 border-primary bg-primary/15 text-primary font-label-caps text-label-caps hover:bg-primary/30 transition-all duration-300 rounded shadow-[0_0_30px_rgba(242,202,80,0.4)] mt-auto gothic-glow-gold disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'ANALYZING...' : 'INITIALIZE SCAN'}
        </button>
      </div>
    </section>
  )
}
