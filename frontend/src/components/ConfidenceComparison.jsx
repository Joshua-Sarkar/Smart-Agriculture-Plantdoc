import '../styles/ConfidenceComparison.css'

function ConfidenceComparison({ aiConfidence, weightedConfidence }) {
  return (
    <div className="confidence-comparison">
      <h3>📊 Confidence Analysis</h3>
      
      <div className="comparison-bars">
        <div className="comparison-item">
          <div className="comparison-label">Raw AI Confidence</div>
          <div className="bar-wrapper">
            <div 
              className="comparison-bar ai-bar"
              style={{ width: `${aiConfidence * 100}%` }}
            >
              <span className="bar-label">{(aiConfidence * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className="comparison-divider"></div>

        <div className="comparison-item">
          <div className="comparison-label">IoT-Weighted Confidence</div>
          <div className="bar-wrapper">
            <div 
              className="comparison-bar weighted-bar"
              style={{ width: `${weightedConfidence * 100}%` }}
            >
              <span className="bar-label">{(weightedConfidence * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="comparison-note">
        <p>💡 <strong>Weighted confidence</strong> adjusts the AI prediction based on real-time environmental conditions from IoT sensors.</p>
      </div>
    </div>
  )
}

export default ConfidenceComparison
