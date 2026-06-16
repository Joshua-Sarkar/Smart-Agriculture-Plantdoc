# PlantDoc Deployment Checklist

## ✅ Project Structure Verification

- [ ] **Backend Directory**
  - [ ] `main.py` - FastAPI application
  - [ ] `inference.py` - TFLite inference engine
  - [ ] `gradcam.py` - Grad-CAM visualization
  - [ ] `iot.py` - IoT sensor simulator
  - [ ] `train.py` - Training script
  - [ ] `requirements.txt` - Dependencies
  - [ ] `model/` directory exists
  - [ ] `dataset/` directory exists
  - [ ] `.env.example` configuration

- [ ] **Frontend Directory**
  - [ ] `src/App.jsx` - Main component
  - [ ] `src/App.css` - Global styles
  - [ ] `src/index.css` - Tailwind imports
  - [ ] `src/components/` directory with 8 components
  - [ ] `src/styles/` directory with 9 CSS files
  - [ ] `package.json` with all dependencies
  - [ ] `vite.config.js` configuration
  - [ ] `tailwind.config.js` configuration
  - [ ] `postcss.config.js` configuration
  - [ ] `.env.example` configuration

- [ ] **Root Level**
  - [ ] `README.md` - Main documentation
  - [ ] `SETUP.md` - Setup guide
  - [ ] `ARCHITECTURE.md` - Technical docs
  - [ ] `.gitignore` - Git ignore rules
  - [ ] `package.json` - Monorepo config
  - [ ] `start-dev.sh` - Dev startup script

## 🔧 Backend Setup Verification

- [ ] Python 3.9+ installed
  ```bash
  python3 --version
  ```

- [ ] Virtual environment created
  ```bash
  cd backend
  python3 -m venv venv
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] All modules import successfully
  ```bash
  python3 -c "import tensorflow; import fastapi; import numpy; import cv2; print('✓ All imports successful')"
  ```

- [ ] API starts without errors
  ```bash
  python -m uvicorn main:app --reload
  # Should show: Uvicorn running on http://127.0.0.1:8000
  ```

- [ ] Swagger UI accessible
  ```bash
  curl http://localhost:8000/docs
  # Should return HTML documentation
  ```

- [ ] Inference engine loads
  ```bash
  # Check for model files if needed
  ls -la model/
  ```

## 🎨 Frontend Setup Verification

- [ ] Node.js 18+ installed
  ```bash
  node --version
  ```

- [ ] npm dependencies installed
  ```bash
  cd frontend
  npm install
  ```

- [ ] Vite dev server starts
  ```bash
  npm run dev
  # Should show: Local: http://localhost:5173
  ```

- [ ] All imports resolve
  ```bash
  npm run lint
  # Should have 0 errors
  ```

- [ ] Tailwind CSS compiled
  ```bash
  # Check that index.css has Tailwind directives
  grep "@tailwind" src/index.css
  ```

- [ ] Components render without errors
  ```bash
  # Check browser console at http://localhost:5173
  ```

## 📊 API Endpoint Verification

- [ ] **POST /analyze** endpoint responds
  ```bash
  # Test with a sample image
  curl -X POST \
    -F "image=@test.jpg" \
    http://localhost:8000/analyze
  ```

- [ ] **GET /health** returns status
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status": "healthy", ...}
  ```

- [ ] **GET /models** returns model info
  ```bash
  curl http://localhost:8000/models
  # Should return model configuration
  ```

- [ ] **GET /diseases** returns class list
  ```bash
  curl http://localhost:8000/diseases
  # Should return list of 38 diseases
  ```

- [ ] **GET /docs** returns Swagger UI
  ```bash
  curl http://localhost:8000/docs
  # Should return HTML
  ```

## 🖼️ Frontend UI Verification

- [ ] **Home page loads** at http://localhost:5173
  - [ ] "PlantDoc" title visible
  - [ ] No console errors

- [ ] **Upload Panel** displays
  - [ ] Drag-and-drop zone visible
  - [ ] Can select files

- [ ] **Results Panel** displays
  - [ ] Shows placeholder text
  - [ ] About button visible

- [ ] **Engine X-Ray Panel** displays
  - [ ] Shows "Analysis details will appear here"
  - [ ] Tech note footer visible

- [ ] **Styling loads correctly**
  - [ ] Dark theme with green accents applied
  - [ ] Responsive layout on small screens
  - [ ] Monospace font for technical values

## 🔗 Integration Verification

- [ ] **Backend running** on port 8000
  ```bash
  lsof -i :8000  # Linux/Mac
  netstat -ano | findstr :8000  # Windows
  ```

- [ ] **Frontend running** on port 5173
  ```bash
  lsof -i :5173
  ```

- [ ] **CORS enabled** in backend
  ```bash
  # Check main.py for CORSMiddleware
  grep "CORSMiddleware" backend/main.py
  ```

- [ ] **API URL configured** in frontend
  ```bash
  # Check .env or App.jsx
  grep "VITE_API_URL" frontend/.env* || grep "API_BASE_URL" frontend/src/App.jsx
  ```

## 🧪 Feature Testing

- [ ] **Image Upload**
  - [ ] Drag image to upload panel
  - [ ] Preview displays
  - [ ] Loading spinner appears

- [ ] **API Response** (requires trained model)
  - [ ] Results populate
  - [ ] Grad-CAM heatmap loads
  - [ ] Confidence values display

- [ ] **UI Animations**
  - [ ] Confidence counters animate
  - [ ] Bars fill with animation
  - [ ] CNN layers light up sequentially

- [ ] **Responsiveness**
  - [ ] Desktop layout works
  - [ ] Tablet layout works (2 columns)
  - [ ] Mobile layout works (1 column)

## 📦 Optional: Model Training Verification

- [ ] **Dataset prepared** in `backend/dataset/`
  - [ ] `train/` subdirectory exists
  - [ ] `val/` subdirectory exists
  - [ ] Disease class folders present

- [ ] **Training runs** without errors
  ```bash
  cd backend
  python train.py
  # Should show training progress
  ```

- [ ] **Models saved**
  - [ ] `model/plant_disease_best.h5` exists
  - [ ] `model/plant_disease_model.tflite` exists
  - [ ] `model/class_indices.json` exists

- [ ] **Model files correct size**
  ```bash
  ls -lh backend/model/
  # .h5 should be ~50MB, .tflite should be ~13MB
  ```

## 🚀 Production Deployment Checklist

- [ ] Environment variables configured
  ```bash
  cp backend/.env.example backend/.env
  cp frontend/.env.example frontend/.env
  # Edit as needed
  ```

- [ ] CORS properly restricted
  - [ ] Update `allow_origins` in main.py to specific domain

- [ ] API rate limiting added (recommended)
  - [ ] Install `slowapi`: `pip install slowapi`
  - [ ] Configure rate limits

- [ ] Authentication added (recommended)
  - [ ] Install `python-jose`: `pip install python-jose passlib`
  - [ ] Add JWT tokens to /analyze endpoint

- [ ] Frontend build tested
  ```bash
  cd frontend
  npm run build
  # Check dist/ folder for minified assets
  ```

- [ ] Docker setup (optional)
  - [ ] Dockerfile created for backend
  - [ ] Docker Compose created for full stack
  - [ ] Images build successfully

- [ ] CI/CD pipeline configured (optional)
  - [ ] GitHub Actions workflow created
  - [ ] Tests run automatically
  - [ ] Deployment automated

## 🐛 Troubleshooting Verification

- [ ] **If models missing**: Run `python train.py`
- [ ] **If imports fail**: Reinstall requirements
- [ ] **If API unreachable**: Check port availability
- [ ] **If frontend won't load**: Check browser console for errors
- [ ] **If styles missing**: Rebuild Tailwind CSS

## ✨ Final Checklist

- [ ] All files created successfully
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] API documentation loads
- [ ] UI renders correctly
- [ ] Ready for testing

---

## 📊 Expected Project Statistics

```
Total Files Created:
  ├─ Backend Python: 5 core + __init__.py
  ├─ Frontend React: 8 components
  ├─ Frontend CSS: 9 component + 1 global
  ├─ Configuration: 8 files
  ├─ Documentation: 5 guides
  └─ Total: 40+ files

Code Quality:
  ├─ Backend: Type hints, docstrings, error handling
  ├─ Frontend: React hooks, component composition
  ├─ Styling: Responsive, dark theme, animations
  └─ Docs: Comprehensive, examples, troubleshooting
```

---

## ✅ Sign-Off

- [ ] I have verified all items above
- [ ] Project is ready for development
- [ ] Documentation is complete
- [ ] Team members have access to setup guide

**Setup Date**: _______________
**Verified By**: _______________
**Notes**: _______________________________________________

---

For questions or issues, refer to:
- Setup Guide: `SETUP.md`
- Architecture: `ARCHITECTURE.md`
- Main README: `README.md`
