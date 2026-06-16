import React, { useEffect, useState, useRef } from 'react'
import gsap from 'gsap'

export default function CNNVisualization({ isAnalyzing }) {
  const [logs, setLogs] = useState([])
  const containerRef = useRef(null)

  useEffect(() => {
    if (!isAnalyzing) {
      setLogs([])
      return
    }

    const timer = setInterval(() => {
      setLogs(prev => {
        const date = new Date()
        const timestamp = `T-MINUS 00:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`
        const x = Math.floor(Math.random() * 800)
        const y = Math.floor(Math.random() * 600)
        
        // Ensure Crimson anomaly every 500ms
        const newLog = {
          time: timestamp,
          msg: `ANOMALY: Spore concentration detected at px(${x},${y}).`,
          type: 'error'
        }
        
        const next = [...prev, newLog]
        if (next.length > 20) next.shift()
        return next
      })
    }, 500)

    return () => clearInterval(timer)
  }, [isAnalyzing])

  // Auto-scroll to bottom
  useEffect(() => {
    if (containerRef.current) {
      gsap.to(containerRef.current, {
        scrollTop: containerRef.current.scrollHeight,
        duration: 0.3,
        ease: "power2.out"
      })
    }
  }, [logs])

  return (
    <>
      <div className="font-label-caps text-label-caps text-sovereign-gold mb-6 uppercase border-b border-sovereign-gold/20 pb-2 shrink-0">Log Stream</div>
      
      <div 
        ref={containerRef}
        className="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar"
      >
        {logs.map((log, i) => (
          <div key={i} className="border-l-2 pl-4 border-error bg-error-container/20 p-2 rounded-r">
            <div className="font-technical-data text-technical-data text-xs mb-1 text-error">
              {log.time}
            </div>
            <div className="font-body-md text-body-md text-error leading-relaxed">
              {log.msg}
            </div>
          </div>
        ))}
        {!isAnalyzing && (
          <div className="border-l-2 border-sovereign-gold/40 pl-4">
            <div className="font-technical-data text-technical-data text-on-surface-variant/80 text-xs mb-1">T-MINUS 00:00:00</div>
            <div className="font-body-md text-body-md text-on-surface">Awaiting target parameters...</div>
          </div>
        )}
      </div>

      <div className="mt-6 pt-6 border-t border-sovereign-gold/20 shrink-0">
        <div className="font-label-caps text-label-caps text-sovereign-gold mb-2 uppercase tracking-[0.2em]">Input Directive</div>
        <div className="relative">
          <input 
            className="w-full bg-transparent border-0 border-b border-sovereign-gold/40 focus:border-moss-green focus:ring-0 text-moss-green font-technical-data px-0 py-2 placeholder:text-on-surface-variant/50 focus:outline-none" 
            placeholder="> AWAITING COMMAND..." 
            type="text"
            readOnly
          />
        </div>
      </div>
    </>
  )
}
