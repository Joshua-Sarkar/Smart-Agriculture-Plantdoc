"""
PlantDoc - Plant Disease Detection API
FastAPI backend for plant disease classification with Grad-CAM visualization and IoT integration
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import List, Dict

# Import our modules
from inference import load_inference_engine
from gradcam import load_gradcam_engine
from iot import get_sensor_readings, get_weighted_confidence

# Initialize FastAPI app
app = FastAPI(
    title="PlantDoc - Plant Disease Detection",
    description="AI-powered plant disease detection with Grad-CAM visualization and IoT sensor integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML engines on startup
inference_engine = None
gradcam_engine = None


@app.on_event("startup")
async def startup_event():
    """Initialize ML engines on startup"""
    global inference_engine, gradcam_engine
    
    print("\n" + "=" * 60)
    print("Starting PlantDoc API")
    print("=" * 60)
    
    # Load inference engine
    print("\nLoading inference engine...")
    inference_engine = load_inference_engine()
    
    if inference_engine:
        print("[OK] Inference engine loaded")
    else:
        print("[WARN] Warning: Could not load inference engine")
    
    # Load Grad-CAM engine
    print("Loading Grad-CAM engine...")
    gradcam_engine = load_gradcam_engine()
    
    if gradcam_engine:
        print("[OK] Grad-CAM engine loaded")
    else:
        print("[WARN] Warning: Could not load Grad-CAM engine")
    
    print("\n" + "=" * 60)
    print("PlantDoc API Ready!")
    print("=" * 60 + "\n")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "PlantDoc API",
        "version": "1.0.0"
    }


@app.post("/analyze")
async def analyze_plant(image: UploadFile = File(...)):
    """
    Analyze plant image for disease
    
    Returns:
        JSON with predictions, confidence, Grad-CAM, and IoT-weighted confidence
    """
    
    # Validate file
    if not image.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    file_ext = image.filename.lower().split('.')[-1]
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Check engines are loaded
    if not inference_engine:
        raise HTTPException(status_code=503, detail="Inference engine not loaded")
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
            contents = await image.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name
        
        # Run inference
        print(f"\n[INFERENCE] Analyzing image: {image.filename}")
        inference_results = inference_engine.run_inference(tmp_path)
        
        # Get top prediction
        top_pred = inference_results['top_prediction']
        disease_name = top_pred['class_name']
        ai_confidence = top_pred['confidence']
        
        print(f"  Top prediction: {disease_name}")
        print(f"  AI confidence: {ai_confidence:.4f}")
        
        # Get Grad-CAM visualization
        print(f"[GRADCAM] Generating attention visualization...")
        gradcam_result = None
        if gradcam_engine:
            try:
                gradcam_result = gradcam_engine.generate_gradcam(
                    tmp_path,
                    pred_index=top_pred['class_index']
                )
                print(f"  [OK] Grad-CAM generated")
            except Exception as e:
                print(f"  [WARN] Error generating Grad-CAM: {e}")
                gradcam_result = None
        
        # Get IoT sensor readings and weighted confidence
        print(f"[IoT] Reading sensors and computing weighted confidence...")
        sensor_readings = get_sensor_readings()
        weighted_confidence_result = get_weighted_confidence(disease_name, ai_confidence)
        
        print(f"  Humidity: {sensor_readings['humidity']:.1f}%")
        print(f"  Temperature: {sensor_readings['temperature']:.1f}°C")
        print(f"  Soil Moisture: {sensor_readings['soil_moisture']:.1f}%")
        print(f"  Weighted confidence: {weighted_confidence_result['weighted_confidence']:.4f}")
        
        # Get disease information
        from iot import confidence_weighter
        disease_info = confidence_weighter.get_disease_info(disease_name)
        
        # Build response
        response = {
            "top_prediction": {
                "class_name": disease_name,
                "class_index": top_pred['class_index'],
                "confidence": ai_confidence
            },
            "top3_predictions": inference_results['top3_predictions'],
            "weighted_confidence": weighted_confidence_result['weighted_confidence'],
            "confidence_factors": weighted_confidence_result['confidence_factors'],
            "sensor_readings": sensor_readings,
            "disease_info": {
                "disease_name": disease_name,
                "description": disease_info.get('description', 'Plant disease detected'),
                "optimal_conditions": disease_info.get('optimal_conditions', {})
            },
            "gradcam_image": gradcam_result['gradcam_image'] if gradcam_result else None,
            "timestamp": sensor_readings['timestamp']
        }
        
        print(f"\n[OK] Analysis complete\n")
        
        return response
        
    except Exception as e:
        print(f"[ERR] Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
        
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "inference_engine": "loaded" if inference_engine else "not loaded",
        "gradcam_engine": "loaded" if gradcam_engine else "not loaded",
        "sensors": "simulated (ready)"
    }


@app.get("/models")
async def get_models_info():
    """Get information about loaded models"""
    return {
        "inference": {
            "model": "TensorFlow Lite",
            "backbone": "EfficientNetB0 (TensorFlow Hub)",
            "classes": 38,
            "status": "loaded" if inference_engine else "not loaded"
        },
        "gradcam": {
            "method": "Class Activation Mapping",
            "layer": "Last convolutional layer of EfficientNetB0",
            "status": "loaded" if gradcam_engine else "not loaded"
        },
        "sensors": {
            "type": "Simulated ESP32",
            "metrics": ["humidity", "temperature", "soil_moisture"],
            "status": "ready"
        }
    }


@app.post("/batch-analyze")
async def batch_analyze(files: List[UploadFile] = File(...)):
    """
    Analyze multiple images
    
    Args:
        files: List of image files
        
    Returns:
        List of analysis results
    """
    results = []
    
    for file in files:
        try:
            result = await analyze_plant(file)
            results.append({
                "filename": file.filename,
                "status": "success",
                "result": result
            })
        except HTTPException as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "error": e.detail
            })
    
    return {"analyses": results}


@app.get("/diseases")
async def get_diseases_list():
    """Get list of all recognized diseases"""
    from inference import PLANT_VILLAGE_CLASSES
    
    return {
        "total_classes": len(PLANT_VILLAGE_CLASSES),
        "diseases": PLANT_VILLAGE_CLASSES
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("Starting PlantDoc API Server")
    print("=" * 60)
    print("\nTo start the server, run:")
    print("  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\nAPI Documentation will be available at:")
    print("  http://localhost:8000/docs")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
