"""
Model Optimization and Compression Utilities

This script provides multiple approaches to reduce model size:
1. Gzip compression (already done)
2. Model quantization (reduces precision)
3. Model pruning (removes less important weights)
4. Model distillation (creates smaller model)
"""

import os
import gzip
import shutil
import sys

def compress_with_7zip():
    """Instructions for using 7-Zip for better compression"""
    print("\n" + "="*60)
    print("7-ZIP COMPRESSION (Better than gzip)")
    print("="*60)
    print("\n1. Download and install 7-Zip from: https://www.7-zip.org/")
    print("\n2. Compress the model:")
    print('   7z a -t7z -mx=9 model_phase1.h5.7z model_phase1.h5')
    print("\n3. This typically achieves 15-25% better compression than gzip")
    print("\n4. To extract:")
    print('   7z e model_phase1.h5.7z')

def model_quantization_example():
    """Show how to quantize a TensorFlow model to reduce size"""
    print("\n" + "="*60)
    print("MODEL QUANTIZATION (Reduces model size significantly)")
    print("="*60)
    print("""
# Install TensorFlow if not already installed
# pip install tensorflow

import tensorflow as tf

# Load your trained model
model = tf.keras.models.load_model('model_phase1.h5')

# Convert to TensorFlow Lite with quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Optional: Use float16 quantization for better accuracy
# converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

# Save the quantized model
with open('model_phase1_quantized.tflite', 'wb') as f:
    f.write(tflite_model)

print("Quantized model saved as model_phase1_quantized.tflite")
""")

def create_download_script():
    """Create a script to download the model if needed"""
    print("\n" + "="*60)
    print("ALTERNATIVE: HOST MODEL EXTERNALLY")
    print("="*60)
    print("\nYou can host the model on:")
    print("1. Google Drive")
    print("2. Dropbox") 
    print("3. AWS S3")
    print("4. GitHub Releases (up to 2GB)")
    print("5. Hugging Face Model Hub")
    
    download_script = '''
import os
import requests
from tqdm import tqdm

def download_model(url, filename):
    """Download model from external source"""
    if os.path.exists(filename):
        print(f"{filename} already exists.")
        return
    
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                pbar.update(len(chunk))
    
    print(f"Downloaded {filename}")

# Example usage:
# download_model("https://your-url/model_phase1.h5.gz", "model_phase1.h5.gz")
'''
    
    with open("download_model.py", "w") as f:
        f.write(download_script)
    
    print("\nCreated download_model.py script for external hosting")

def check_alternatives():
    """Check what files we have and suggest best approach"""
    print("\n" + "="*60)
    print("CURRENT FILE SIZES")
    print("="*60)
    
    files_to_check = [
        "model_phase1.h5",
        "model_phase1.h5.gz", 
        "best_model.h5"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"{filename}: {size / (1024*1024):.2f} MB")
    
    print("\n" + "="*60)
    print("RECOMMENDED SOLUTIONS")
    print("="*60)
    print("\n1. BEST: Use Git LFS (shown above)")
    print("2. Try 7-Zip compression (better than gzip)")
    print("3. Use model quantization (TensorFlow Lite)")
    print("4. Host model externally and download when needed")
    print("5. Use GitHub Releases (supports up to 2GB files)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "7zip":
            compress_with_7zip()
        elif sys.argv[1] == "quantize":
            model_quantization_example()
        elif sys.argv[1] == "download":
            create_download_script()
    else:
        check_alternatives()