"""
Plant Disease Classification - The Chaos Pipeline
Uses EfficientNetB0, dynamic class detection, and extreme OpenCV data augmentation.
"""

import os
import cv2
import json
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- CONFIGURATION ---
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS_FROZEN = 10
EPOCHS_FINE_TUNE = 15
DATASET_PATH = "dataset"
MODEL_PATH = "model"

def apply_chaos_to_image(image):
    """
    The brutal real-world simulator. 
    Mangles pristine lab photos so the AI survives contact with the internet.
    """
    # 1. The "Toxic Ex" (Random Cutout)
    if np.random.rand() > 0.5:
        h, w = image.shape[:2]
        y = np.random.randint(0, max(1, h - 50))
        x = np.random.randint(0, max(1, w - 50))
        image[y:y+50, x:x+50, :] = 0 
        
    # 2. The "Deep-Fried Simulator" (Compression)
    if np.random.rand() > 0.5:
        small = cv2.resize(image, (56, 56), interpolation=cv2.INTER_LINEAR)
        image = cv2.resize(small, (224, 224), interpolation=cv2.INTER_NEAREST)
        
    # 3. The "Bad Sensor" (Gaussian Noise)
    if np.random.rand() > 0.5:
        noise = np.random.normal(0, 10, image.shape)
        image = np.clip(image + noise, 0, 255).astype(np.float32)
        
    return image

def load_data():
    """Load dataset, automatically split 80/20, and apply chaos to training only."""
    
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH)
        print(f"⚠️ Created empty '{DATASET_PATH}' directory. Put your folders inside!")
        return None, None, None

    print("🔍 Scanning biological material...")

    # The Torture Chamber (For Training Only)
    train_datagen = ImageDataGenerator(
        rotation_range=40,
        brightness_range=[0.5, 1.5],
        zoom_range=[0.8, 1.2],
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.3,
        horizontal_flip=True,
        fill_mode='nearest',
        preprocessing_function=apply_chaos_to_image,
        validation_split=0.2 # Reserve 20% for the polygraph test
    )
    
    # The Polygraph Test (Pure, unadulterated validation data)
    val_datagen = ImageDataGenerator(validation_split=0.2)
    
    try:
        train_data = train_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training'
        )
        
        val_data = val_datagen.flow_from_directory(
            DATASET_PATH,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation'
        )
        
        return train_data, val_data, train_data.class_indices
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None, None, None

def build_model(num_classes):
    """Build model with EfficientNetB0 backbone"""
    efficientnet_url = "https://tfhub.dev/google/efficientnet/b0/feature-vector/1"
    
    model = keras.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.Rescaling(1./127.5, offset=-1),
        hub.KerasLayer(efficientnet_url, trainable=False),
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(1e-4)),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

def compile_model(model, learning_rate=1e-3):
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

def train():
    print("=" * 60)
    print("🌿 PlantDoc AI - Commencing Neural Training Protocol")
    print("=" * 60)
    
    train_data, val_data, class_indices = load_data()
    if train_data is None:
        return
    
    num_classes = len(class_indices)
    print(f"🧠 Detected {num_classes} distinct diseases/classes.")
    
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    model = build_model(num_classes)
    compile_model(model, learning_rate=1e-3)
    
    checkpoint_cb = keras.callbacks.ModelCheckpoint(
        os.path.join(MODEL_PATH, 'plant_disease_best.h5'),
        monitor='val_accuracy', save_best_only=True, mode='max', verbose=1
    )
    early_stop_cb = keras.callbacks.EarlyStopping(
        monitor='val_accuracy', patience=3, restore_best_weights=True, verbose=1
    )
    
    print(f"\n[PHASE 1] Training outer cortex (Frozen Backbone) for {EPOCHS_FROZEN} epochs...")
    model.fit(train_data, epochs=EPOCHS_FROZEN, validation_data=val_data, callbacks=[checkpoint_cb, early_stop_cb])
    
    print(f"\n[PHASE 2] Unlocking deep memory (Fine-tuning) for {EPOCHS_FINE_TUNE} epochs...")
    for layer in model.layers:
        if isinstance(layer, hub.KerasLayer):
            layer.trainable = True
            break
            
    compile_model(model, learning_rate=1e-5)
    model.fit(train_data, epochs=EPOCHS_FINE_TUNE, validation_data=val_data, callbacks=[checkpoint_cb, early_stop_cb])
    
    # Reload best model and convert to TFLite
    print("\n🗜️ Compressing brain into TFLite format...")
    best_model = keras.models.load_model(
        os.path.join(MODEL_PATH, 'plant_disease_best.h5'),
        custom_objects={'KerasLayer': hub.KerasLayer}
    )
    
    converter = tf.lite.TFLiteConverter.from_keras_model(best_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    # Save the artifacts
    tflite_path = os.path.join(MODEL_PATH, 'plant_disease_model.tflite')
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
        
    class_indices_path = os.path.join(MODEL_PATH, 'class_indices.json')
    with open(class_indices_path, 'w') as f:
        json.dump({v: k for k, v in class_indices.items()}, f) # Map index -> class name
        
    print(f"\n✅ TFLite model saved to: {tflite_path}")
    print(f"✅ Class map saved to: {class_indices_path}")
    print("=" * 60)
    print("🎉 Training Complete. The entity is ready to judge leaves.")

if __name__ == "__main__":
    train()