# PlantDoc Setup Guide

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- pip (Python package manager)
- npm or yarn (JavaScript package manager)

## 🔧 Installation

### 1. Clone or Download PlantDoc

```bash
cd plantdoc
```

### 2. Backend Setup

#### Option A: Automatic Setup (Linux/Mac)
```bash
chmod +x start-dev.sh
./start-dev.sh
```

#### Option B: Manual Setup

**Create Python virtual environment:**
```bash
cd backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Configure environment:**
```bash
cp .env.example .env
# Edit .env if needed
```

**Start API server:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure API URL (optional)
cp .env.example .env
# Edit .env if your backend is not on localhost:8000

# Start development server
npm run dev
```

## 🎬 Running the Application

### Backend
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python -m uvicorn main:app --reload
```

API available at: **http://localhost:8000**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend
```bash
cd frontend
npm run dev
```

Frontend available at: **http://localhost:5173**

## 📊 Training Your Own Model

### 1. Prepare Dataset

Download the PlantVillage dataset or your own plant disease images and structure as:

```
backend/dataset/
├── train/
│   ├── Apple___Apple_scab/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── Apple___Black_rot/
│   ├── ... (other classes)
│   └── Tomato___healthy/
└── val/
    ├── Apple___Apple_scab/
    ├── Apple___Black_rot/
    ├── ... (other classes)
    └── Tomato___healthy/
```

### 2. Train Model

```bash
cd backend
python train.py
```

This will:
- Load EfficientNetB0 from TensorFlow Hub
- Apply data augmentation
- Train with frozen backbone (10 epochs)
- Fine-tune with unfrozen backbone (15 epochs)
- Save best model to `model/plant_disease_best.h5`
- Export to TFLite: `model/plant_disease_model.tflite`

### 3. Test Inference

```bash
python inference.py
```

## 🚀 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

Output: `frontend/dist/` folder ready for deployment

### Backend Deployment

**Using Docker:**
```bash
docker build -t plantdoc-backend .
docker run -p 8000:8000 plantdoc-backend
```

**Using Gunicorn (production WSGI server):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'tensorflow'"**
```bash
# Reinstall dependencies
pip install --upgrade tensorflow tensorflow-hub
```

**"Model not found" error**
```bash
# Make sure you have:
# 1. Trained the model: python train.py
# 2. Or downloaded a pre-trained model to backend/model/
```

**CORS errors**
```bash
# The API has CORS enabled for all origins
# If issues persist, check CORS middleware in main.py
```

### Frontend Issues

**"Cannot find module" error**
```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
```

**API connection errors**
```bash
# Check .env file
cat .env

# Ensure backend is running
# If backend is on different host:
VITE_API_URL=http://your-backend-host:8000
```

**Tailwind styles not loading**
```bash
# Rebuild Tailwind CSS
npm run dev  # Should auto-rebuild
# Or manually: npx tailwindcss -i ./src/index.css -o ./dist/output.css
```

## 📊 API Usage Examples

### Analyze an Image

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "image=@path/to/image.jpg" \
  http://localhost:8000/analyze
```

### Get Supported Diseases

```bash
curl http://localhost:8000/diseases
```

### Get Model Info

```bash
curl http://localhost:8000/models
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🔒 Security Notes

1. **API Keys**: Add authentication before production
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **CORS**: Restrict CORS origins to your frontend domain
4. **Data Privacy**: Handle user images securely (temporary storage only)
5. **Model Security**: Ensure model files are protected

## 📈 Performance Tips

### Backend Optimization
- Use GPU support for TensorFlow (CUDA)
- Deploy multiple API instances behind load balancer
- Use Redis for caching

### Frontend Optimization
- Enable gzip compression
- Use CDN for static assets
- Lazy load components

## 🔍 Development Tools

### API Testing
- Postman: https://www.postman.com/
- Thunder Client: VS Code extension
- cURL: Command line

### Frontend Debugging
- React Developer Tools: Chrome extension
- Redux DevTools: Debug state management

## 📚 Additional Resources

- **TensorFlow Hub**: https://tfhub.dev/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/

## ❓ FAQ

**Q: Can I use a different pre-trained model?**
A: Yes! Modify `train.py` to load a different model from TensorFlow Hub.

**Q: How do I add more disease classes?**
A: Add more folders to the dataset directory and retrain the model.

**Q: Can I run this on a Raspberry Pi?**
A: Yes! Use TFLite with NNAPI acceleration or Edge TPU for optimized inference.

**Q: How do I add authentication?**
A: Install `python-jose` and `passlib`, then add JWT tokens to FastAPI endpoints.

---

For more help, see the main README.md or open an issue on GitHub.
