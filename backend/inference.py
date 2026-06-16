"""
Plant Disease Inference - TFLite Model Inference
Loads TFLite model and performs inference on input images
"""

import numpy as np
import tensorflow as tf
from PIL import Image
import json
import os

MODEL_PATH = "model"
TFLITE_MODEL = os.path.join(MODEL_PATH, "plant_disease_model.tflite")
CLASS_INDICES_PATH = os.path.join(MODEL_PATH, "class_indices.json")
IMG_SIZE = 224

# PlantVillage disease class names (38 classes)
PLANT_VILLAGE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]


class PlantDiseaseInference:
    def __init__(self):
        """Initialize the inference engine with TFLite model"""
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.class_names = PLANT_VILLAGE_CLASSES
        self._load_model()
    
    def _load_model(self):
        """Load TFLite model"""
        if not os.path.exists(TFLITE_MODEL):
            raise FileNotFoundError(f"TFLite model not found at {TFLITE_MODEL}")
        
        self.interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        print(f"[OK] Loaded TFLite model from {TFLITE_MODEL}")
    
    def preprocess_image(self, image_path):
        """
        Load and preprocess image to 224×224
        
        Args:
            image_path (str): Path to input image
            
        Returns:
            preprocessed_image (np.ndarray): Image array ready for inference
            original_image (PIL.Image): Original image for visualization
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        
        # Resize to 224x224
        image = original_image.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize to [-1, 1]
        image_array = np.array(image, dtype=np.float32)
        image_array = (image_array / 127.5) - 1.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array, original_image
    
    def run_inference(self, image_path):
        """
        Run inference on image and get top-3 predictions
        
        Args:
            image_path (str): Path to input image
            
        Returns:
            dict: Contains top_prediction, confidence, top3_predictions with scores
        """
        # Preprocess image
        preprocessed_image, original_image = self.preprocess_image(image_path)
        
        # Run inference
        self.interpreter.set_tensor(self.input_details[0]['index'], preprocessed_image)
        self.interpreter.invoke()
        
        # Get output
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        predictions = output_data[0]  # Remove batch dimension
        
        # Get top-3 predictions
        top_3_indices = np.argsort(predictions)[-3:][::-1]
        
        results = {
            'top_prediction': {
                'class_name': self.class_names[top_3_indices[0]],
                'class_index': int(top_3_indices[0]),
                'confidence': float(predictions[top_3_indices[0]])
            },
            'top3_predictions': [],
            'all_predictions': predictions.tolist(),
            'original_image': original_image
        }
        
        # Add top-3 predictions
        for idx, class_idx in enumerate(top_3_indices):
            results['top3_predictions'].append({
                'rank': idx + 1,
                'class_name': self.class_names[class_idx],
                'class_index': int(class_idx),
                'confidence': float(predictions[class_idx])
            })
        
        return results


def load_inference_engine():
    """Factory function to load inference engine"""
    try:
        engine = PlantDiseaseInference()
        return engine
    except Exception as e:
        print(f"Error loading inference engine: {e}")
        return None


if __name__ == "__main__":
    # Test inference (requires a test image)
    print("Plant Disease Inference Engine")
    print("=" * 60)
    
    engine = load_inference_engine()
    
    if engine:
        test_image_path = "test_image.jpg"  # Placeholder
        
        if os.path.exists(test_image_path):
            results = engine.run_inference(test_image_path)
            
            print(f"\nTop Prediction: {results['top_prediction']['class_name']}")
            print(f"Confidence: {results['top_prediction']['confidence']:.4f}")
            print("\nTop-3 Predictions:")
            for pred in results['top3_predictions']:
                print(f"  {pred['rank']}. {pred['class_name']}: {pred['confidence']:.4f}")
        else:
            print(f"Test image not found at {test_image_path}")
