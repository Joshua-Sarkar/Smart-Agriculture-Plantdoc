"""
Grad-CAM Visualization for Plant Disease Model
Generates attention heatmaps showing model focus areas
"""

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
from PIL import Image
import base64
import io
import os

MODEL_PATH = "model"
KERAS_MODEL_PATH = os.path.join(MODEL_PATH, "plant_disease_best.keras")
IMG_SIZE = 224


class GradCAM:
    def __init__(self):
        """Initialize Grad-CAM for EfficientNetB0 model"""
        self.model = self._load_model()
        self.effnet_submodel = None      # The EfficientNetB0 sub-model
        self.head_layers = []            # Layers after EfficientNetB0
        self.last_conv_layer_name = None
        self.gradcam_model = True        # Flag - signals engine is ready
        self._setup_gradcam_components()

    def _load_model(self):
        """Load the Keras model for gradient computation"""
        if not os.path.exists(KERAS_MODEL_PATH):
            print(f"[WARN] Keras model not found at {KERAS_MODEL_PATH}")
            return None

        try:
            model = tf.keras.models.load_model(
                KERAS_MODEL_PATH,
                custom_objects={'KerasLayer': hub.KerasLayer}
            )
            print(f"[OK] Loaded Keras model from {KERAS_MODEL_PATH}")
            return model
        except Exception as e:
            print(f"[ERR] Error loading model: {e}")
            return None

    def _setup_gradcam_components(self):
        """
        Identify the EfficientNetB0 sub-model and head layers.
        Also find the name of the last Conv2D layer inside EfficientNetB0.
        """
        if self.model is None:
            self.gradcam_model = None
            return

        # Find the backbone sub-model
        for layer in self.model.layers:
            if isinstance(layer, hub.KerasLayer):
                self.effnet_submodel = layer
                self.last_conv_layer_name = None  # hub layers handled differently
                print(f"[OK] Backbone: hub.KerasLayer '{layer.name}'")
                break
            elif hasattr(layer, 'layers') and len(getattr(layer, 'layers', [])) > 5:
                self.effnet_submodel = layer
                # Find the last Conv2D inside the sub-model
                for sublayer in reversed(layer.layers):
                    if isinstance(sublayer, tf.keras.layers.Conv2D):
                        self.last_conv_layer_name = sublayer.name
                        break
                print(f"[OK] Backbone: '{layer.name}', last conv: '{self.last_conv_layer_name}'")
                break

        if self.effnet_submodel is None:
            print("[WARN] Could not find backbone sub-model - GradCAM heatmaps disabled")
            self.gradcam_model = None
            return

        # Collect the head layers (everything after the backbone)
        backbone_found = False
        for layer in self.model.layers:
            if layer is self.effnet_submodel:
                backbone_found = True
                continue
            if backbone_found:
                self.head_layers.append(layer)

        print(f"[OK] GradCAM setup complete. Head layers: {[l.name for l in self.head_layers]}")

    def generate_gradcam(self, image_path, pred_index=None):
        """
        Generate Grad-CAM heatmap for given image

        Args:
            image_path (str): Path to input image
            pred_index (int): Index of class to generate gradcam for

        Returns:
            dict: Contains gradcam_image (base64), heatmap, and original image
        """
        if self.model is None or self.gradcam_model is None:
            return None

        # Load and preprocess image
        original_image = Image.open(image_path).convert('RGB')
        image = original_image.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
        image_array = np.array(image, dtype=np.float32)
        image_array = (image_array / 127.5) - 1.0
        image_tensor = tf.expand_dims(image_array, axis=0)

        try:
            if self.last_conv_layer_name is not None:
                # Case 1: Functional sub-model - capture last conv via sub-model feature extractor
                conv_layer = self.effnet_submodel.get_layer(self.last_conv_layer_name)
                feature_extractor = tf.keras.Model(
                    inputs=self.effnet_submodel.input,
                    outputs=[conv_layer.output, self.effnet_submodel.output]
                )

                with tf.GradientTape() as tape:
                    conv_outputs, backbone_features = feature_extractor(image_tensor)
                    tape.watch(conv_outputs)

                    # Pass through head layers to get final predictions
                    x = backbone_features
                    for layer in self.head_layers:
                        x = layer(x)
                    predictions = x

                    if pred_index is None:
                        pred_index = int(tf.argmax(predictions[0]))
                    class_channel = predictions[:, pred_index]

                grads = tape.gradient(class_channel, conv_outputs)

            else:
                # Case 2: hub.KerasLayer - use input gradients as fallback heatmap
                with tf.GradientTape() as tape:
                    tape.watch(image_tensor)
                    predictions = self.model(image_tensor)
                    if pred_index is None:
                        pred_index = int(tf.argmax(predictions[0]))
                    class_channel = predictions[:, pred_index]

                grads = tape.gradient(class_channel, image_tensor)
                conv_outputs = tf.abs(grads)
                grads = tf.ones_like(grads)

            if grads is None:
                print("[WARN] GradCAM: gradients are None")
                return None

            # Compute weighted activation map
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            conv_map = conv_outputs[0]
            heatmap = conv_map @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-10)
            heatmap = heatmap.numpy()

            # Handle edge case where heatmap might be a scalar
            if heatmap.ndim == 0:
                heatmap = np.ones((7, 7)) * float(heatmap)

            # Resize and colorize
            heatmap_resized = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE))
            heatmap_uint8 = np.uint8(255 * heatmap_resized)
            heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

            image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            overlay = cv2.addWeighted(image_bgr, 0.5, heatmap_colored, 0.5, 0)
            overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

            pil_image = Image.fromarray(overlay_rgb)
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

            return {
                'gradcam_image': f"data:image/png;base64,{img_base64}",
                'heatmap': heatmap_resized.tolist(),
                'heatmap_max': float(np.max(heatmap_resized)),
                'heatmap_min': float(np.min(heatmap_resized)),
                'overlay': overlay_rgb
            }

        except Exception as e:
            print(f"[WARN] GradCAM generation error: {e}")
            return None

    def generate_multi_gradcam(self, image_path, top_n=3):
        """
        Generate Grad-CAM heatmaps for top-N predictions

        Args:
            image_path (str): Path to input image
            top_n (int): Number of top predictions to visualize

        Returns:
            dict: Contains gradcam images for top-N predictions
        """
        results = {}

        for i in range(top_n):
            gradcam_result = self.generate_gradcam(image_path, pred_index=i)
            if gradcam_result:
                results[f'top_{i+1}'] = gradcam_result

        return results


def load_gradcam_engine():
    """Factory function to load Grad-CAM engine"""
    try:
        engine = GradCAM()
        return engine
    except Exception as e:
        print(f"[ERR] Error loading Grad-CAM engine: {e}")
        return None


if __name__ == "__main__":
    print("Grad-CAM Visualization Engine")
    print("=" * 60)

    engine = load_gradcam_engine()

    if engine:
        test_image_path = "test_image.jpg"

        if os.path.exists(test_image_path):
            results = engine.generate_gradcam(test_image_path)

            if results:
                print("[OK] Grad-CAM heatmap generated successfully")
                print(f"  Heatmap shape: {np.array(results['heatmap']).shape}")
                print(f"  Image encoding: {results['gradcam_image'][:50]}...")
        else:
            print(f"Test image not found at {test_image_path}")
