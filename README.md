# PlantDoc — AI Plant Disease Analysis

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/repositories/plantdoc/hero.gif" width="100%" alt="PlantDoc animated botanical AI banner" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Joshua-Sarkar/Joshua-Sarkar/media/repositories/plantdoc/flow.gif" width="100%" alt="PlantDoc image inference, Grad-CAM and environmental context workflow" />
</p>

PlantDoc is a full-stack smart-agriculture project combining leaf-image classification, model explainability and simulated environmental sensor context. The current label set follows the **38 PlantVillage classes** included in the inference module.

## Core features

- **Leaf-image classification:** a TensorFlow Lite interpreter expects a 224×224 RGB image, normalises pixel values to `[-1, 1]`, and returns class scores for the 38 configured labels.
- **Top predictions:** the API returns the leading prediction and additional ranked predictions so the result is not reduced to a single label.
- **Grad-CAM:** a separate Keras model is used to generate a heatmap/overlay illustrating which image regions influenced the model's class score.
- **Environmental context:** an ESP32-style simulator produces humidity, temperature and soil-moisture readings with controlled variation.
- **Confidence weighting:** disease-specific environmental ranges are compared with the simulated readings to calculate an additional context score.
- **Interactive frontend:** React/Vite presents the uploaded image, prediction, heatmap, environmental readings and model explanations.

## How the pipeline works

1. A user uploads a leaf image in the React interface.
2. The frontend posts it to FastAPI's `/analyze` endpoint.
3. The backend validates the file and runs TFLite inference.
4. The predicted class is used to request a Grad-CAM overlay from the separate Keras model.
5. The IoT simulator produces environmental readings and the weighting module compares them with the selected disease profile.
6. The API returns prediction, top classes, sensor readings, weighted score and visualisation data.

The environmental score is a simulated context layer. It should not be treated as a real field sensor reading or as a clinical/agronomic diagnosis.

## API endpoints

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Backend health/status |
| POST | `/analyze` | Analyse one uploaded plant image |
| GET | `/health` | Health check |
| GET | `/models` | Model engine status |
| POST | `/analyze/batch` | Batch image analysis |
| GET | `/diseases` | Return supported disease labels |

FastAPI's interactive API documentation is available at `/docs` when the backend is running.

## Repository map

- `backend/main.py` — FastAPI routes and orchestration
- `backend/inference.py` — TFLite image preprocessing and classification
- `backend/gradcam.py` — Keras/Grad-CAM heatmap generation
- `backend/iot.py` — sensor simulator and environmental weighting
- `backend/train.py` — training/export workflow
- `frontend/` — React + Vite application
- `ARCHITECTURE.md` — detailed architecture notes
- `SETUP.md` — setup and troubleshooting guide

## Run locally

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm
- Model files in the paths expected by the backend

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

In a second terminal:

```bash
cd frontend
npm install
# Optional: create .env and set VITE_API_URL if the backend is not on localhost:8000
npm run dev
```

Open the Vite URL printed by the dev server (normally `http://localhost:5173`). The frontend expects the backend at `http://localhost:8000` unless configured otherwise.

### Model files

The inference code expects `backend/model/plant_disease_model.tflite` and `backend/model/class_indices.json`; Grad-CAM expects `backend/model/plant_disease_best.keras`. These weights are not included in the tracked source tree. Train/export or place the corresponding model files in those locations before expecting inference to start.

## Limitations

- The 38-class model is constrained by its training data and may not generalise to field conditions, camera types or unseen diseases.
- Grad-CAM is an explanatory visualisation, not proof that the model reasoned correctly.
- Sensor readings are simulated; no physical ESP32 device is connected by the current `iot.py` module.
- A high model score is not an agronomist's diagnosis. Treat results as decision support for experimentation, not treatment instructions.

---

<p align="center"><sub>Read the leaf. Inspect the heatmap. Check the environment.</sub></p>
