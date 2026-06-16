import '../styles/AboutModel.css'

function AboutModel({ onClose }) {
  return (
    <div className="about-overlay" onClick={onClose}>
      <div className="about-modal" onClick={(e) => e.stopPropagation()}>
        <div className="about-header">
          <h2>🎓 About This Model</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="about-content">
          <section className="about-section">
            <h3>🔄 Transfer Learning</h3>
            <p>
              This model uses <strong>EfficientNetB0</strong>, a neural network pre-trained on 14 million images from ImageNet. Instead of training from scratch, we leverage this existing knowledge and fine-tune it for plant diseases. This approach is 1000x faster and requires far less data than training from scratch. The model's backbone is frozen initially, then gradually unfrozen for fine-tuning, preserving learned features while adapting to plant pathology.
            </p>
          </section>

          <section className="about-section">
            <h3>🎯 Grad-CAM Visualization</h3>
            <p>
              Grad-CAM (Gradient-weighted Class Activation Mapping) shows <strong>where the neural network focuses</strong> when making predictions. By computing gradients of the predicted class with respect to the last convolutional layer, we generate a heatmap showing which regions of your leaf image are most important for the diagnosis. This provides interpretability — you can verify the model is looking at the right symptoms.
            </p>
          </section>

          <section className="about-section">
            <h3>🔗 IoT Sensor Integration & Bayesian Weighting</h3>
            <p>
              The raw AI confidence is adjusted using <strong>real-time environmental data</strong> (humidity, temperature, soil moisture). Each disease thrives in specific conditions. Late Blight needs high humidity, while Powdery Mildew prefers dry air. Using Bayesian weighting, we compute how compatible the current environment is with the detected disease, creating a <strong>weighted confidence score</strong> that reflects both visual evidence and environmental likelihood.
            </p>
          </section>

          <section className="about-section tech-specs">
            <h3>🛠️ Technical Stack</h3>
            <ul>
              <li><strong>Backbone:</strong> EfficientNetB0 (from TensorFlow Hub)</li>
              <li><strong>Classes:</strong> 38 plant diseases (PlantVillage dataset)</li>
              <li><strong>Inference:</strong> TensorFlow Lite (optimized for edge)</li>
              <li><strong>Frontend:</strong> React + Vite + Tailwind CSS</li>
              <li><strong>Backend:</strong> FastAPI + Python</li>
            </ul>
          </section>
        </div>

        <div className="about-footer">
          <button className="close-button" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  )
}

export default AboutModel
