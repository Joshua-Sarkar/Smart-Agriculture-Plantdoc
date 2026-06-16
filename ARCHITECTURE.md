# PlantDoc Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                      │
│  ┌──────────────────┬──────────────────┬──────────────────┐  │
│  │  Upload Panel    │  Results Panel   │  Engine X-Ray    │  │
│  │  - Drag & Drop   │  - Grad-CAM      │  - CNN Pipeline  │  │
│  │  - Preview       │  - Disease Name  │  - IoT Gauges    │  │
│  │                  │  - Top-3 Bars    │  - Comparison    │  │
│  └──────────────────┴──────────────────┴──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             ▼ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  POST /analyze                                       │  │
│  │  ├─ Inference Engine (TFLite)                       │  │
│  │  ├─ Grad-CAM Engine                                │  │
│  │  ├─ IoT Sensor Simulator                           │  │
│  │  └─ Bayesian Confidence Weighter                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             ▼ ML/Data
┌─────────────────────────────────────────────────────────────┐
│                    ML Models & Data                           │
│  ├─ EfficientNetB0 (TensorFlow Hub)                        │
│  ├─ TFLite Model (13MB, optimized)                         │
│  ├─ PlantVillage Dataset (38 classes)                      │
│  └─ Disease Environmental Requirements DB                  │
└─────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Core Components

#### 1. **Inference Engine** (`inference.py`)
```
Image Input (224×224)
    ↓
[Preprocessing: Normalize to [-1, 1]]
    ↓
[TFLite Model Execution]
    ↓
[38-class Output: Softmax probabilities]
    ↓
[Post-processing: Top-3 predictions]
    ↓
Results {class_name, confidence, class_index}
```

**Key Points:**
- Uses TFLite for 50MB→13MB model compression
- INT8 quantization with DEFAULT optimization
- Batch size: 1 (per-request inference)
- Input: 224×224×3 RGB image
- Output: [38] probability vector

#### 2. **Grad-CAM Engine** (`gradcam.py`)
```
Image + Keras Model
    ↓
[Forward pass to last Conv layer]
    ↓
[Compute class gradients with GradientTape]
    ↓
[Global average pooling of gradients]
    ↓
[Heatmap generation via linear combination]
    ↓
[Normalize & scale to [0, 255]]
    ↓
[Apply JET colormap]
    ↓
[50% overlay with original image]
    ↓
[Encode as base64 PNG]
    ↓
Data URL for frontend display
```

**Mathematical Formula:**
```
Attention = ReLU(Σ α_k * A_k)

Where:
- α_k = (1/Z) * Σ_ij (∂y_c / ∂A_ij^k) = Global average pool of gradients
- A_k = k-th feature map of last conv layer
- y_c = predicted class score
```

#### 3. **IoT Sensor Simulator** (`iot.py`)
```
Simulated ESP32 Readings
├─ Humidity: 65% ± 3% (Gaussian noise)
├─ Temperature: 22°C ± 1.5°C
└─ Soil Moisture: 60% ± 4%

        ↓

Disease Environmental Requirements
├─ Late Blight: Humidity 85-100%, Temp 12-22°C, Moisture 70-100%
├─ Powdery Mildew: Humidity 40-80%, Temp 15-28°C, Moisture 20-60%
└─ [36 other diseases...]

        ↓

Bayesian Confidence Computation
P(Disease | Sensors) = ∏(P(Sensor | Disease requirements))^(1/3)

Where each factor is:
P(humidity | disease) = exp(-(humidity - optimal)² / 2σ²)
σ = range_width / 3

        ↓

Weighted Confidence: 0.0 - 1.0
```

#### 4. **Main API** (`main.py`)
```
POST /analyze
    ↓
[Receive multipart image]
    ↓
[Validate file type]
    ↓
[Save to temporary file]
    ↓
[Run inference pipeline]
    │
    ├─→ Inference: class_name, confidence
    │
    ├─→ Grad-CAM: heatmap overlay
    │
    └─→ IoT+Weighting: sensor readings, weighted confidence
    ↓
[Combine results into JSON]
    ↓
[Return response]
    ↓
[Clean up temp file]
    ↓
200 OK + JSON response
```

### Data Flow

#### Training Pipeline
```
PlantVillage Dataset
    ├─ 80% Training data
    └─ 20% Validation data
            ↓
[Data Augmentation]
├─ Rotation: ±40°
├─ Brightness: 0.8-1.2x
├─ Zoom: ±20%
├─ Shifts: ±20%
└─ Horizontal flip
            ↓
[Model Architecture]
├─ Input: 224×224×3
├─ EfficientNetB0 backbone
├─ GlobalAveragePooling2D
├─ Dropout(0.3)
├─ Dense(256, relu)
├─ Dropout(0.2)
└─ Dense(38, softmax)
            ↓
[Two-Phase Training]
├─ Phase 1 (10 epochs): Frozen backbone
│   └─ LR: 1e-3, Optimizer: Adam
└─ Phase 2 (15 epochs): Fine-tuned backbone
    └─ LR: 1e-5, Optimizer: Adam
            ↓
[Model Checkpoint]
└─ Save best model → plant_disease_best.h5
            ↓
[TFLite Conversion]
├─ Optimization: DEFAULT
├─ Ops: TFLITE_BUILTINS + SELECT_TF_OPS
└─ Output: plant_disease_model.tflite (13MB)
```

## Frontend Architecture

### Component Hierarchy

```
App.jsx (Main orchestrator)
├─ State:
│  ├─ image: {file, preview}
│  ├─ analysisResults: API response
│  ├─ loading: boolean
│  └─ error: string
│
├─ Effects:
│  └─ Fetch from API_BASE_URL
│
└─ Children:
   ├─ UploadPanel
   │  ├─ State: handleDragOver, handleDrop
   │  ├─ UI:
   │  │  ├─ Empty: Upload zone (dashed border)
   │  │  └─ Filled: Image preview + loading spinner
   │  └─ Events: onUpload → parent
   │
   ├─ ResultsPanel
   │  ├─ Props: image, results, loading, error
   │  ├─ State: showAbout (modal)
   │  ├─ Children:
   │  │  ├─ GradCAM image display
   │  │  ├─ CountUpConfidence
   │  │  │  └─ Animated counter (0→confidence)
   │  │  ├─ Top3Predictions
   │  │  │  └─ Animated bars
   │  │  ├─ Disease info section
   │  │  └─ AboutModel (conditional)
   │  └─ UI: Dark card layout
   │
   └─ EngineXRay
      ├─ Props: results, isAnalyzing
      ├─ Children:
      │  ├─ CNNVisualization
      │  │  └─ Animated layer blocks (Input→Output)
      │  ├─ IoTGauges
      │  │  └─ 3 circular progress indicators
      │  └─ ConfidenceComparison
      │     └─ Before/after bars
      └─ UI: Dashboard style
```

### Styling Architecture

```
CSS Hierarchy:
├─ App.css (global variables, layout)
│  ├─ :root variables (colors, fonts)
│  ├─ @keyframes (animations)
│  └─ Responsive breakpoints
│
├─ Component CSS files:
│  ├─ UploadPanel.css
│  ├─ ResultsPanel.css
│  ├─ CountUpConfidence.css
│  ├─ Top3Predictions.css
│  ├─ EngineXRay.css
│  ├─ CNNVisualization.css
│  ├─ IoTGauges.css
│  ├─ ConfidenceComparison.css
│  └─ AboutModel.css
│
└─ Tailwind configuration:
   ├─ tailwind.config.js (content, theme)
   └─ postcss.config.js (plugins)
```

**Color Scheme:**
```
--dark-bg: #0f172a (Page background)
--card-bg: #1e293b (Card background)
--primary-green: #10b981 (Main accent)
--primary-green-light: #6ee7b7 (Highlights)
--accent-cyan: #06b6d4 (AI confidence)
--accent-purple: #a855f7 (Weighted confidence)
--text-primary: #f1f5f9 (Main text)
--text-secondary: #cbd5e1 (Secondary text)
```

## API Specification

### POST /analyze

**Request:**
```
Content-Type: multipart/form-data

Body:
- image: File (JPG, PNG, BMP, GIF)
```

**Response (200 OK):**
```json
{
  "top_prediction": {
    "class_name": "Tomato___Late_blight",
    "class_index": 30,
    "confidence": 0.92
  },
  "top3_predictions": [
    {
      "rank": 1,
      "class_name": "Tomato___Late_blight",
      "class_index": 30,
      "confidence": 0.92
    },
    {
      "rank": 2,
      "class_name": "Tomato___Early_blight",
      "class_index": 29,
      "confidence": 0.065
    },
    {
      "rank": 3,
      "class_name": "Tomato___healthy",
      "class_index": 37,
      "confidence": 0.013
    }
  ],
  "weighted_confidence": 0.88,
  "confidence_factors": {
    "humidity_fit": 0.95,
    "temperature_fit": 0.78,
    "moisture_fit": 0.92,
    "combined_fit": 0.88,
    "sensor_readings": {
      "humidity": 85.2,
      "temperature": 18.5,
      "soil_moisture": 65.3,
      "timestamp": "2026-05-06T08:30:00"
    },
    "requirements": {
      "humidity_optimal_range": [85, 100],
      "temperature_optimal_range": [12, 22],
      "moisture_optimal_range": [70, 100]
    }
  },
  "sensor_readings": {
    "humidity": 85.2,
    "temperature": 18.5,
    "soil_moisture": 65.3,
    "timestamp": "2026-05-06T08:30:00"
  },
  "disease_info": {
    "disease_name": "Tomato___Late_blight",
    "description": "Caused by Phytophthora infestans. Requires cool, wet conditions.",
    "optimal_conditions": {
      "humidity": "85-100%",
      "temperature": "12-22°C",
      "soil_moisture": "70-100%"
    }
  },
  "gradcam_image": "data:image/png;base64,...",
  "timestamp": "2026-05-06T08:30:00"
}
```

## Performance Characteristics

### Inference Pipeline Timing (GPU)
```
Image Loading:         20ms
Preprocessing:         30ms
TFLite Inference:     100-150ms
Grad-CAM:             100-200ms
IoT + Weighting:       50ms
JSON Serialization:    50ms
─────────────────────────────
Total:                350-500ms
```

### Model Metrics
```
Backbone: EfficientNetB0
├─ Parameters: 5.3M
├─ Keras: 50MB
├─ TFLite: 13MB (74% compression)
├─ Latency (CPU): 1-2s
└─ Latency (GPU): 200-500ms

Classification Head:
├─ GlobalAveragePooling2D: 2048→1
├─ Dense(256, relu): 2048→256
└─ Dense(38, softmax): 256→38
```

### Frontend Metrics
```
Bundle Size:
├─ React: 42KB
├─ Vite: 0KB (dev only)
├─ Tailwind: 8KB (purged)
├─ Custom CSS: 25KB
└─ Total: ~75KB gzipped

Initial Load: 1-2s
Interaction: <100ms
Memory: 50-100MB (typical browser)
```

## Security Architecture

```
Input Validation:
├─ File type checking (image/* MIME type)
├─ File size limits (max 20MB)
└─ Path traversal prevention

Data Privacy:
├─ Temporary file cleanup (immediate)
├─ No persistent storage of user images
└─ CORS headers for frontend only

Model Security:
├─ Read-only model files
├─ No model download endpoints
└─ Inference-only API (no training)

API Security:
├─ Rate limiting (future)
├─ Authentication tokens (future)
└─ HTTPS in production (recommended)
```

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
    ↓
┌───────────────────────────┐
│  API Instance 1 (port 8000)
│  API Instance 2 (port 8001)
│  API Instance 3 (port 8002)
│  API Instance 4 (port 8003)
└───────────────────────────┘
    ↓
[Redis Cache]
    ↓
[Shared Model Storage]
```

### Vertical Scaling
```
Single Instance Optimization:
├─ GPU support (CUDA/TensorRT)
├─ TFLite NNAPI acceleration
├─ Model quantization (INT8)
└─ Batch inference (future)
```

## Deployment Architectures

### Development
```
Local Machine
├─ Backend: localhost:8000
├─ Frontend: localhost:5173
└─ Direct communication
```

### Production (Docker)
```
Docker Container
├─ Python 3.9 slim image
├─ TensorFlow (CPU/GPU)
├─ FastAPI + Uvicorn
└─ Exposed port 8000
```

### Cloud (AWS/GCP/Azure)
```
Load Balancer (Application Layer)
    ↓
├─ Auto-scaling group of containers
├─ Each with TFLite model
├─ Shared model registry
└─ CloudSQL database (future)
```

---

**Architecture Version**: 1.0  
**Last Updated**: May 2026  
**Contact**: architecture@plantdoc.ai
