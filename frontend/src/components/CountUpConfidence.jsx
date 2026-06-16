import { useState, useEffect } from 'react'
import '../styles/CountUpConfidence.css'

function CountUpConfidence({ confidence, weightedConfidence }) {
  const [displayAI, setDisplayAI] = useState(0)
  const [displayWeighted, setDisplayWeighted] = useState(0)

  useEffect(() => {
    if (confidence) {
      let start = 0
      const end = Math.floor(confidence * 100)
      const duration = 1500
      const increment = end / (duration / 16)
      
      let current = start
      const timer = setInterval(() => {
        current += increment
        if (current >= end) {
          setDisplayAI(end)
          clearInterval(timer)
        } else {
          setDisplayAI(Math.floor(current))
        }
      }, 16)
      
      return () => clearInterval(timer)
    }
  }, [confidence])

  useEffect(() => {
    if (weightedConfidence) {
      let start = 0
      const end = Math.floor(weightedConfidence * 100)
      const duration = 1500
      const delay = 300
      const increment = end / (duration / 16)
      
      const startTimer = setTimeout(() => {
        let current = start
        const timer = setInterval(() => {
          current += increment
          if (current >= end) {
            setDisplayWeighted(end)
            clearInterval(timer)
          } else {
            setDisplayWeighted(Math.floor(current))
          }
        }, 16)
        
        return () => clearInterval(timer)
      }, delay)
      
      return () => clearTimeout(startTimer)
    }
  }, [weightedConfidence])

  return (
    <div className="confidence-container">
      <div className="confidence-card ai-confidence">
        <div className="confidence-label">🤖 AI Confidence</div>
        <div className="confidence-value">{displayAI}%</div>
        <div className="confidence-bar">
          <div 
            className="confidence-fill ai-fill" 
            style={{ width: `${displayAI}%` }}
          ></div>
        </div>
      </div>

      <div className="confidence-card weighted-confidence">
        <div className="confidence-label">🔗 IoT-Weighted</div>
        <div className="confidence-value">{displayWeighted}%</div>
        <div className="confidence-bar">
          <div 
            className="confidence-fill weighted-fill" 
            style={{ width: `${displayWeighted}%` }}
          ></div>
        </div>
      </div>
    </div>
  )
}

export default CountUpConfidence
