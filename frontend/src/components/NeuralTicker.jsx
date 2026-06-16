import React, { useState, useEffect, useRef } from 'react';
import gsap from 'gsap';

const NeuralTicker = ({ isAnalyzing, results }) => {
  const [logs, setLogs] = useState([]);
  const tickerRef = useRef(null);

  useEffect(() => {
    let interval;
    if (isAnalyzing) {
      interval = setInterval(() => {
        setLogs(prev => {
          const rawVal = (Math.random() * 8 - 4).toFixed(4); // Simulated logit
          const tensor = `[T${Math.floor(Math.random() * 9000) + 1000}]`;
          const str = `${tensor} RAW_LOGIT: ${rawVal > 0 ? '+' : ''}${rawVal}`;
          const next = [...prev, str];
          if (next.length > 15) next.shift(); // Keep latest 15
          return next;
        });
      }, 300);
    } else if (results) {
      const conf = results.top_prediction.confidence;
      const safeConf = Math.min(Math.max(conf, 0.001), 0.999);
      const finalLogit = Math.log(safeConf / (1 - safeConf)).toFixed(4);
      setLogs([`[INFERENCE COMPLETE] FINAL LOGIT MATRIX: +${finalLogit} (CONFIDENCE: ${(conf * 100).toFixed(3)}%)`]);
    } else {
      setLogs(["[SYSTEM] NEURAL ENGINE IDLE. AWAITING SPECIMEN..."]);
    }
    return () => clearInterval(interval);
  }, [isAnalyzing, results]);

  // GSAP subtle pulse for the ticker text
  useEffect(() => {
    if (tickerRef.current) {
      gsap.to(tickerRef.current, {
        opacity: 0.8,
        yoyo: true,
        repeat: -1,
        duration: 2,
        ease: 'power1.inOut'
      });
    }
  }, []);

  return (
    <div className="fixed bottom-0 left-0 right-0 h-8 bg-black border-t border-[var(--gold-dim)] z-50 overflow-hidden flex items-center shadow-[0_-5px_20px_rgba(212,175,55,0.1)]">
      <div 
        ref={tickerRef} 
        className="whitespace-nowrap flex gap-12 animate-[scroll_20s_linear_infinite]"
        style={{ animationPlayState: isAnalyzing ? 'running' : 'paused' }}
      >
        {[...Array(4)].map((_, i) => (
          <div key={i} className="flex gap-12">
            {logs.map((log, j) => (
              <span key={`${i}-${j}`} className="text-[10px] text-[var(--sovereign-gold)] font-mono opacity-80 uppercase tracking-widest">
                {log}
              </span>
            ))}
          </div>
        ))}
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}} />
    </div>
  );
};

export default NeuralTicker;
