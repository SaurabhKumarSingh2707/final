import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.optimizers import AdamW
import numpy as np
import os
import matplotlib.pyplot as plt

# Enhanced constants
IMG_HEIGHT = 300  # Increased image size for better feature extraction
IMG_WIDTH = 300
BATCH_SIZE = 8    # Reduced batch size due to larger model
TRAIN_DIR = 'train'

class AdvancedDataAugmentation:
    """Advanced data augmentation techniques"""
    
    @staticmethod
    def get_train_augmentation():
        """Get training data augmentation pipeline"""
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        
        return ImageDataGenerator(
            rescale=1./255,
            rotation_range=30,
            width_shift_range=0.3,
            height_shift_range=0.3,
            shear_range=0.3,
            zoom_range=0.3,
            channel_shift_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            brightness_range=[0.7, 1.3],
            fill_mode='reflect',  # Better than 'nearest' for plant images
            validation_split=0.15  # Smaller validation split for tiny dataset
        )
    
    @staticmethod
    def get_validation_augmentation():
        """Get validation data augmentation (minimal)"""
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        
        return ImageDataGenerator(
            rescale=1./255,
            validation_split=0.15
        )

def create_advanced_model(num_classes, input_shape=(300, 300, 3)):
    """
    Create an advanced model using ResNet50V2 with progressive training
    """
    # Use ResNet50V2 for better accuracy and stability
    base_model = ResNet50V2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Initially freeze base model
    base_model.trainable = False
    
    # Add custom classification head with attention mechanism
    inputs = keras.Input(shape=input_shape)
    x = base_model(inputs, training=False)
    
    # Global Average Pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Attention mechanism (simple)
    attention = layers.Dense(x.shape[-1], activation='sigmoid')(x)
    x = layers.Multiply()([x, attention])
    
    # Dense layers with batch normalization and dropout
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    return model, base_model

def create_data_generators():
    """Create enhanced data generators with heavy augmentation"""
    
    train_datagen = AdvancedDataAugmentation.get_train_augmentation()
    val_datagen = AdvancedDataAugmentation.get_validation_augmentation()
    
    # Training generator with heavy augmentation
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True,
        seed=42
    )
    
    # Validation generator
    validation_generator = val_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
        seed=42
    )
    
    return train_generator, validation_generator

def compute_class_weights(train_generator):
    """Compute class weights to handle class imbalance"""
    
    # Get class indices and labels
    class_indices = train_generator.class_indices
    classes = list(class_indices.keys())
    
    # Count samples per class in training set
    class_counts = {}
    for class_name in classes:
        class_dir = os.path.join(TRAIN_DIR, class_name)
        class_counts[class_name] = len(os.listdir(class_dir))
    
    # Calculate class weights
    total_samples = sum(class_counts.values())
    num_classes = len(classes)
    
    class_weights = {}
    for i, class_name in enumerate(classes):
        # Inverse frequency weighting
        weight = total_samples / (num_classes * class_counts[class_name])
        class_weights[i] = weight
    
    print("Class weights:")
    for i, class_name in enumerate(classes):
        if i < 5:  # Print first 5
            print(f"  {class_name}: {class_weights[i]:.2f}")
    print(f"  ... and {len(classes)-5} more")
    
    return class_weights

def cosine_annealing_schedule(epoch, lr):
    """Cosine annealing learning rate schedule"""
    epochs = 100
    min_lr = 1e-7
    max_lr = 1e-3
    
    return min_lr + (max_lr - min_lr) * 0.5 * (1 + np.cos(np.pi * epoch / epochs))

def create_advanced_callbacks():
    """Create advanced callbacks for training"""
    
    callbacks = [
        # Early stopping with more patience for small dataset
        EarlyStopping(
            monitor='val_loss',
            patience=20,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Learning rate scheduling
        LearningRateScheduler(cosine_annealing_schedule, verbose=1),
        
        # Model checkpointing
        ModelCheckpoint(
            'best_model_advanced.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1,
            save_weights_only=False
        ),
        
        # Reduce learning rate on plateau (backup)
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.3,
            patience=8,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    return callbacks

class TestTimeAugmentation:
    """Test-time augmentation for improved inference"""
    
    def __init__(self, model, num_augmentations=5):
        self.model = model
        self.num_augmentations = num_augmentations
    
    def predict_with_tta(self, image_array):
        """Make predictions with test-time augmentation"""
        predictions = []
        
        # Original image
        pred = self.model.predict(image_array, verbose=0)
        predictions.append(pred)
        
        # Augmented versions
        for _ in range(self.num_augmentations - 1):
            augmented = self._augment_image(image_array[0])
            augmented = np.expand_dims(augmented, axis=0)
            pred = self.model.predict(augmented, verbose=0)
            predictions.append(pred)
        
        # Average predictions
        final_prediction = np.mean(predictions, axis=0)
        return final_prediction
    
    def _augment_image(self, image):
        """Apply random augmentations to image"""
        # Random rotation
        angle = np.random.uniform(-15, 15)
        image = tf.keras.preprocessing.image.apply_affine_transform(
            image, theta=angle, fill_mode='reflect'
        )
        
        # Random brightness
        brightness = np.random.uniform(0.8, 1.2)
        image = tf.image.adjust_brightness(image, brightness - 1.0)
        
        # Random zoom
        zoom = np.random.uniform(0.9, 1.1)
        if zoom != 1.0:
            image = tf.keras.preprocessing.image.apply_affine_transform(
                image, zx=zoom, zy=zoom, fill_mode='reflect'
            )
        
        return np.clip(image, 0, 1)

def train_advanced_model():
    """Train the advanced model with progressive training"""
    
    print("Creating advanced data generators...")
    train_generator, validation_generator = create_data_generators()
    
    num_classes = train_generator.num_classes
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print(f"Number of classes: {num_classes}")
    
    # Compute class weights
    class_weights = compute_class_weights(train_generator)
    
    print("\nCreating advanced model...")
    model, base_model = create_advanced_model(num_classes)
    
    # Phase 1: Train only the classification head
    print("\n" + "="*50)
    print("PHASE 1: Training classification head only")
    print("="*50)
    
    model.compile(
        optimizer=AdamW(learning_rate=1e-3, weight_decay=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    callbacks_phase1 = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        ModelCheckpoint('model_phase1.h5', monitor='val_accuracy', save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=5, min_lr=1e-6)
    ]
    
    history1 = model.fit(
        train_generator,
        epochs=40,
        validation_data=validation_generator,
        callbacks=callbacks_phase1,
        class_weight=class_weights,
        verbose=1
    )
    
    # Phase 2: Fine-tune the entire model
    print("\n" + "="*50)
    print("PHASE 2: Fine-tuning entire model")
    print("="*50)
    
    # Unfreeze the base model
    base_model.trainable = True
    
    # Use a much lower learning rate for fine-tuning
    model.compile(
        optimizer=AdamW(learning_rate=1e-5, weight_decay=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    callbacks_phase2 = create_advanced_callbacks()
    
    history2 = model.fit(
        train_generator,
        epochs=60,
        validation_data=validation_generator,
        callbacks=callbacks_phase2,
        class_weight=class_weights,
        verbose=1
    )
    
    # Save final model
    model.save('plant_disease_model_advanced.h5')
    print("Advanced model saved as 'plant_disease_model_advanced.h5'")
    
    # Save class names
    class_names = list(train_generator.class_indices.keys())
    with open('class_names_advanced.txt', 'w') as f:
        for class_name in class_names:
            f.write(class_name + '\n')
    
    # Evaluate final model
    print("\nFinal evaluation:")
    val_loss, val_accuracy = model.evaluate(validation_generator, verbose=0)
    print(f"Validation Loss: {val_loss:.4f}")
    print(f"Validation Accuracy: {val_accuracy:.4f}")
    
    # Plot training history
    plot_advanced_training_history(history1, history2)
    
    return model, (history1, history2)

def plot_advanced_training_history(history1, history2):
    """Plot training history for both phases"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Combine histories
    epochs1 = len(history1.history['accuracy'])
    epochs2 = len(history2.history['accuracy'])
    
    total_epochs = list(range(1, epochs1 + 1)) + list(range(epochs1 + 1, epochs1 + epochs2 + 1))
    
    accuracy = history1.history['accuracy'] + history2.history['accuracy']
    val_accuracy = history1.history['val_accuracy'] + history2.history['val_accuracy']
    loss = history1.history['loss'] + history2.history['loss']
    val_loss = history1.history['val_loss'] + history2.history['val_loss']
    
    # Plot accuracy
    axes[0, 0].plot(total_epochs, accuracy, label='Training Accuracy', color='blue')
    axes[0, 0].plot(total_epochs, val_accuracy, label='Validation Accuracy', color='red')
    axes[0, 0].axvline(x=epochs1, color='green', linestyle='--', alpha=0.7, label='Fine-tuning starts')
    axes[0, 0].set_title('Model Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot loss
    axes[0, 1].plot(total_epochs, loss, label='Training Loss', color='blue')
    axes[0, 1].plot(total_epochs, val_loss, label='Validation Loss', color='red')
    axes[0, 1].axvline(x=epochs1, color='green', linestyle='--', alpha=0.7, label='Fine-tuning starts')
    axes[0, 1].set_title('Model Loss')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot learning rate changes
    axes[1, 0].plot(total_epochs, [1e-3]*epochs1 + [1e-5]*epochs2, label='Learning Rate', color='green')
    axes[1, 0].axvline(x=epochs1, color='green', linestyle='--', alpha=0.7, label='Fine-tuning starts')
    axes[1, 0].set_title('Learning Rate Schedule')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Learning Rate')
    axes[1, 0].set_yscale('log')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Learning rate plot (if available)
    axes[1, 1].text(0.5, 0.5, 'Advanced Model Training\n\nPhase 1: Head training\nPhase 2: Full fine-tuning\n\nFeatures:\n• ResNet50V2 backbone\n• Advanced data augmentation\n• Class weighting\n• Progressive training', 
                   transform=axes[1, 1].transAxes, fontsize=12, ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    axes[1, 1].set_title('Training Summary')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('advanced_training_history.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Set GPU memory growth
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
    
    print("Starting Advanced Plant Disease Model Training...")
    print("Features: ResNet50V2, Progressive Training, Advanced Augmentation, Class Weighting")
    
    try:
        model, history = train_advanced_model()
        print("\n🎉 Advanced model training completed successfully!")
        print("✅ Model saved as 'plant_disease_model_advanced.h5'")
        print("✅ Best weights saved as 'best_model_advanced.h5'")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()