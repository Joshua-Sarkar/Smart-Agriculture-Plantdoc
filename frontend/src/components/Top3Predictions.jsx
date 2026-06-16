import '../styles/Top3Predictions.css'

function Top3Predictions({ predictions }) {
  return (
    <div className="top3-section">
      <h3>🎯 Top 3 Predictions</h3>
      <div className="predictions-list">
        {predictions.map((pred, idx) => (
          <div key={idx} className="prediction-item">
            <div className="prediction-rank">#{pred.rank}</div>
            <div className="prediction-name">
              {pred.class_name.replace(/_/g, ' ')}
            </div>
            <div className="prediction-bar-container">
              <div 
                className="prediction-bar"
                style={{ 
                  width: `${pred.confidence * 100}%`,
                  animation: `fillBar 0.8s ease-out ${idx * 0.15}s both`
                }}
              ></div>
            </div>
            <div className="prediction-score">
              {(pred.confidence * 100).toFixed(1)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Top3Predictions
