"""
IoT Sensor Integration and Bayesian Confidence Weighting
Simulates ESP32 sensor readings and provides environment-based confidence adjustments
"""

import random
import numpy as np
from typing import Dict, Tuple


class SensorSimulator:
    """Simulates ESP32 sensor readings"""
    
    def __init__(self, base_humidity=65, base_temp=22, base_moisture=60):
        """
        Initialize sensor simulator with base values
        
        Args:
            base_humidity (float): Base humidity percentage (0-100)
            base_temp (float): Base temperature in Celsius
            base_moisture (float): Base soil moisture percentage (0-100)
        """
        self.base_humidity = base_humidity
        self.base_temp = base_temp
        self.base_moisture = base_moisture
    
    def read_sensors(self):
        """
        Simulate ESP32 sensor readings with random variation
        
        Returns:
            dict: Sensor readings with slight random variation
        """
        # Add Gaussian noise (±5% or ±2°C)
        humidity = np.clip(
            self.base_humidity + np.random.normal(0, 3),
            0, 100
        )
        temperature = self.base_temp + np.random.normal(0, 1.5)
        soil_moisture = np.clip(
            self.base_moisture + np.random.normal(0, 4),
            0, 100
        )
        
        return {
            'humidity': float(humidity),
            'temperature': float(temperature),
            'soil_moisture': float(soil_moisture),
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def update_base_values(self, humidity=None, temp=None, moisture=None):
        """Update base sensor values"""
        if humidity is not None:
            self.base_humidity = np.clip(humidity, 0, 100)
        if temp is not None:
            self.base_temp = temp
        if moisture is not None:
            self.base_moisture = np.clip(moisture, 0, 100)


# Disease environmental requirements (based on PlantVillage dataset)
DISEASE_ENVIRONMENTAL_REQUIREMENTS = {
    # Apple diseases
    "Apple___Apple_scab": {
        "humidity_range": (60, 100),  # Needs high humidity
        "temp_range": (4, 24),         # Moderate temperatures
        "moisture_range": (40, 100)    # Moderate to high moisture
    },
    "Apple___Black_rot": {
        "humidity_range": (70, 100),   # Requires high humidity
        "temp_range": (15, 27),        # Warm
        "moisture_range": (50, 100)
    },
    "Apple___Cedar_apple_rust": {
        "humidity_range": (50, 100),
        "temp_range": (10, 25),
        "moisture_range": (40, 100)
    },
    "Apple___healthy": {
        "humidity_range": (30, 80),    # Moderate conditions
        "temp_range": (15, 28),
        "moisture_range": (30, 70)
    },
    
    # Blueberry
    "Blueberry___healthy": {
        "humidity_range": (40, 75),
        "temp_range": (15, 25),
        "moisture_range": (40, 70)
    },
    
    # Cherry (Powdery Mildew)
    "Cherry_(including_sour)___Powdery_mildew": {
        "humidity_range": (50, 90),    # Moderate humidity
        "temp_range": (15, 27),
        "moisture_range": (20, 60)     # DRY conditions preferred
    },
    "Cherry_(including_sour)___healthy": {
        "humidity_range": (35, 70),
        "temp_range": (15, 25),
        "moisture_range": (35, 65)
    },
    
    # Corn
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "humidity_range": (70, 100),   # High humidity
        "temp_range": (20, 30),        # Warm
        "moisture_range": (60, 100)
    },
    "Corn_(maize)___Common_rust": {
        "humidity_range": (70, 95),
        "temp_range": (15, 25),
        "moisture_range": (50, 100)
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "humidity_range": (80, 100),
        "temp_range": (15, 25),
        "moisture_range": (60, 100)
    },
    "Corn_(maize)___healthy": {
        "humidity_range": (40, 70),
        "temp_range": (18, 28),
        "moisture_range": (50, 80)
    },
    
    # Grape
    "Grape___Black_rot": {
        "humidity_range": (80, 100),   # High humidity
        "temp_range": (20, 30),        # Warm
        "moisture_range": (60, 100)
    },
    "Grape___Esca_(Black_Measles)": {
        "humidity_range": (70, 100),
        "temp_range": (15, 28),
        "moisture_range": (50, 100)
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "humidity_range": (85, 100),
        "temp_range": (18, 26),
        "moisture_range": (65, 100)
    },
    "Grape___healthy": {
        "humidity_range": (40, 75),
        "temp_range": (15, 28),
        "moisture_range": (40, 70)
    },
    
    # Orange (Citrus Greening)
    "Orange___Haunglongbing_(Citrus_greening)": {
        "humidity_range": (60, 95),
        "temp_range": (20, 32),
        "moisture_range": (50, 90)
    },
    
    # Peach
    "Peach___Bacterial_spot": {
        "humidity_range": (75, 100),
        "temp_range": (18, 28),
        "moisture_range": (55, 100)
    },
    "Peach___healthy": {
        "humidity_range": (35, 70),
        "temp_range": (15, 27),
        "moisture_range": (40, 70)
    },
    
    # Pepper
    "Pepper,_bell___Bacterial_spot": {
        "humidity_range": (80, 100),
        "temp_range": (20, 30),
        "moisture_range": (60, 100)
    },
    "Pepper,_bell___healthy": {
        "humidity_range": (40, 75),
        "temp_range": (18, 28),
        "moisture_range": (45, 75)
    },
    
    # Potato
    "Potato___Early_blight": {
        "humidity_range": (80, 100),
        "temp_range": (15, 27),
        "moisture_range": (60, 100)
    },
    "Potato___Late_blight": {
        "humidity_range": (85, 100),   # VERY high humidity
        "temp_range": (12, 22),        # Cool
        "moisture_range": (70, 100)
    },
    "Potato___healthy": {
        "humidity_range": (45, 75),
        "temp_range": (15, 25),
        "moisture_range": (50, 80)
    },
    
    # Raspberry
    "Raspberry___healthy": {
        "humidity_range": (40, 75),
        "temp_range": (15, 25),
        "moisture_range": (45, 75)
    },
    
    # Soybean
    "Soybean___healthy": {
        "humidity_range": (45, 75),
        "temp_range": (18, 28),
        "moisture_range": (50, 80)
    },
    
    # Squash (Powdery Mildew)
    "Squash___Powdery_mildew": {
        "humidity_range": (40, 80),    # Moderate
        "temp_range": (15, 28),
        "moisture_range": (20, 50)     # DRY
    },
    
    # Strawberry
    "Strawberry___Leaf_scorch": {
        "humidity_range": (75, 100),
        "temp_range": (18, 28),
        "moisture_range": (60, 100)
    },
    "Strawberry___healthy": {
        "humidity_range": (40, 75),
        "temp_range": (15, 25),
        "moisture_range": (45, 75)
    },
    
    # Tomato diseases
    "Tomato___Bacterial_spot": {
        "humidity_range": (80, 100),
        "temp_range": (20, 30),
        "moisture_range": (65, 100)
    },
    "Tomato___Early_blight": {
        "humidity_range": (75, 100),
        "temp_range": (15, 27),
        "moisture_range": (60, 100)
    },
    "Tomato___Late_blight": {
        "humidity_range": (85, 100),
        "temp_range": (12, 23),
        "moisture_range": (70, 100)
    },
    "Tomato___Leaf_Mold": {
        "humidity_range": (85, 100),
        "temp_range": (18, 28),
        "moisture_range": (65, 100)
    },
    "Tomato___Septoria_leaf_spot": {
        "humidity_range": (80, 100),
        "temp_range": (15, 28),
        "moisture_range": (60, 100)
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "humidity_range": (20, 60),    # LOW humidity
        "temp_range": (20, 35),        # Hot and dry
        "moisture_range": (10, 40)
    },
    "Tomato___Target_Spot": {
        "humidity_range": (80, 100),
        "temp_range": (20, 28),
        "moisture_range": (60, 100)
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "humidity_range": (40, 80),
        "temp_range": (20, 32),
        "moisture_range": (30, 70)
    },
    "Tomato___Tomato_mosaic_virus": {
        "humidity_range": (50, 85),
        "temp_range": (15, 28),
        "moisture_range": (40, 80)
    },
    "Tomato___healthy": {
        "humidity_range": (40, 75),
        "temp_range": (18, 28),
        "moisture_range": (50, 75)
    },
}


class BayesianConfidenceWeighter:
    """
    Computes environment-aware confidence scores using Bayesian weighting
    Adjusts AI predictions based on sensor readings and disease requirements
    """
    
    def __init__(self):
        """Initialize the weighter"""
        self.requirements = DISEASE_ENVIRONMENTAL_REQUIREMENTS
    
    def compute_weighted_confidence(self, disease_name: str, sensor_readings: Dict) -> Tuple[float, Dict]:
        """
        Compute Bayesian-weighted confidence based on environmental conditions
        
        Args:
            disease_name (str): Name of detected disease
            sensor_readings (dict): Contains humidity, temperature, soil_moisture
            
        Returns:
            tuple: (weighted_confidence, confidence_factors)
        """
        if disease_name not in self.requirements:
            return 1.0, {"error": "Disease not found in requirements"}
        
        requirements = self.requirements[disease_name]
        
        # Extract sensor values
        humidity = sensor_readings.get('humidity', 50)
        temperature = sensor_readings.get('temperature', 22)
        soil_moisture = sensor_readings.get('soil_moisture', 50)
        
        # Compute Gaussian likelihood for each factor
        humidity_likelihood = self._compute_gaussian_likelihood(
            humidity,
            requirements['humidity_range']
        )
        
        temp_likelihood = self._compute_gaussian_likelihood(
            temperature,
            requirements['temp_range']
        )
        
        moisture_likelihood = self._compute_gaussian_likelihood(
            soil_moisture,
            requirements['moisture_range']
        )
        
        # Bayesian combination (geometric mean for better numerical stability)
        weighted_confidence = (
            humidity_likelihood * 
            temp_likelihood * 
            moisture_likelihood
        ) ** (1/3)
        
        # Ensure result is between 0 and 1
        weighted_confidence = np.clip(weighted_confidence, 0.0, 1.0)
        
        confidence_factors = {
            'humidity_fit': float(humidity_likelihood),
            'temperature_fit': float(temp_likelihood),
            'moisture_fit': float(moisture_likelihood),
            'combined_fit': float(weighted_confidence),
            'sensor_readings': sensor_readings,
            'requirements': {
                'humidity_optimal_range': list(requirements['humidity_range']),
                'temperature_optimal_range': list(requirements['temp_range']),
                'moisture_optimal_range': list(requirements['moisture_range'])
            }
        }
        
        return weighted_confidence, confidence_factors
    
    def _compute_gaussian_likelihood(self, value: float, optimal_range: Tuple[float, float]) -> float:
        """
        Compute Gaussian likelihood given value and optimal range
        
        Args:
            value (float): Measured value
            optimal_range (tuple): (min, max) of optimal range
            
        Returns:
            float: Likelihood score between 0 and 1
        """
        range_min, range_max = optimal_range
        range_center = (range_min + range_max) / 2
        range_width = (range_max - range_min) / 2
        
        # Sigma is 1/3 of range width (covers ±3 sigma within range)
        sigma = range_width / 3
        
        # Compute Gaussian probability
        likelihood = np.exp(-((value - range_center) ** 2) / (2 * sigma ** 2))
        
        return float(likelihood)
    
    def get_disease_info(self, disease_name: str) -> Dict:
        """
        Get environmental requirements and info for a disease
        
        Args:
            disease_name (str): Name of disease
            
        Returns:
            dict: Disease information and requirements
        """
        if disease_name not in self.requirements:
            return {"error": "Disease not found"}
        
        requirements = self.requirements[disease_name]
        
        return {
            'disease_name': disease_name,
            'optimal_conditions': {
                'humidity': f"{requirements['humidity_range'][0]}-{requirements['humidity_range'][1]}%",
                'temperature': f"{requirements['temp_range'][0]}-{requirements['temp_range'][1]}°C",
                'soil_moisture': f"{requirements['moisture_range'][0]}-{requirements['moisture_range'][1]}%"
            },
            'description': self._get_disease_description(disease_name)
        }
    
    def _get_disease_description(self, disease_name: str) -> str:
        """Get brief description of disease"""
        descriptions = {
            "Potato___Late_blight": "Caused by Phytophthora infestans. Requires cool, wet conditions.",
            "Tomato___Late_blight": "Caused by Phytophthora infestans. Requires cool, wet conditions.",
            "Squash___Powdery_mildew": "Fungal disease. Prefers dry, moderate conditions.",
            "Tomato___Spider_mites Two-spotted_spider_mite": "Pest. Thrives in hot, dry conditions.",
            "Apple___Apple_scab": "Fungal disease. Needs moisture for spore dispersal.",
        }
        
        return descriptions.get(disease_name, "Plant disease detected.")


# Global instances
sensor_sim = SensorSimulator()
confidence_weighter = BayesianConfidenceWeighter()


def get_sensor_readings():
    """Get current sensor readings"""
    return sensor_sim.read_sensors()


def get_weighted_confidence(disease_name: str, ai_confidence: float = None) -> Dict:
    """
    Get environment-weighted confidence for a disease
    
    Args:
        disease_name (str): Predicted disease name
        ai_confidence (float): Original AI model confidence (optional)
        
    Returns:
        dict: Weighted confidence and factors
    """
    sensor_readings = get_sensor_readings()
    weighted_conf, factors = confidence_weighter.compute_weighted_confidence(
        disease_name, 
        sensor_readings
    )
    
    return {
        'disease_name': disease_name,
        'ai_confidence': ai_confidence,
        'weighted_confidence': weighted_conf,
        'confidence_factors': factors,
        'sensor_readings': sensor_readings
    }


if __name__ == "__main__":
    print("IoT Sensor and Bayesian Weighting Engine")
    print("=" * 60)
    
    # Simulate sensor readings
    for i in range(3):
        readings = get_sensor_readings()
        print(f"\nReading {i+1}:")
        print(f"  Humidity: {readings['humidity']:.1f}%")
        print(f"  Temperature: {readings['temperature']:.1f}°C")
        print(f"  Soil Moisture: {readings['soil_moisture']:.1f}%")
    
    # Test weighting
    print("\n" + "=" * 60)
    print("Testing Confidence Weighting:\n")
    
    test_diseases = ["Potato___Late_blight", "Tomato___healthy", "Squash___Powdery_mildew"]
    
    for disease in test_diseases:
        result = get_weighted_confidence(disease, ai_confidence=0.92)
        print(f"Disease: {disease}")
        print(f"  AI Confidence: {result['ai_confidence']:.4f}")
        print(f"  Weighted Confidence: {result['weighted_confidence']:.4f}")
        print(f"  Humidity Fit: {result['confidence_factors']['humidity_fit']:.4f}")
        print(f"  Temperature Fit: {result['confidence_factors']['temperature_fit']:.4f}")
        print(f"  Moisture Fit: {result['confidence_factors']['moisture_fit']:.4f}\n")
