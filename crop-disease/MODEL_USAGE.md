# Model Files and Usage

This repository contains crop disease detection models. Due to GitHub's file size limitations, large model files are stored using Git LFS (Large File Storage).

## Model Files

- `best_model.h5` (12.84 MB) - Optimized model, directly available
- `model_phase1.h5.gz` (141.62 MB) - Compressed version of the phase 1 model
- `model_phase1.h5` (152.03 MB) - Original phase 1 model (Git LFS tracked)

## Using the Compressed Model

### Option 1: Decompress the .gz file

```python
# Run the decompression script
python compress_model.py decompress
```

### Option 2: Load compressed model directly (if using in production)

```python
import gzip
import tempfile
import tensorflow as tf

def load_compressed_model(compressed_path):
    """Load a model from a gzipped file"""
    with gzip.open(compressed_path, 'rb') as f_in:
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as f_out:
            f_out.write(f_in.read())
            temp_path = f_out.name
    
    model = tf.keras.models.load_model(temp_path)
    os.unlink(temp_path)  # Clean up temp file
    return model

# Usage
model = load_compressed_model('model_phase1.h5.gz')
```

## Git LFS Setup (for contributors)

If you're cloning this repository:

1. Make sure Git LFS is installed: `git lfs install`
2. Clone the repository: `git clone <repo-url>`
3. Pull LFS files: `git lfs pull`

## Model Compression

The repository includes utilities for model compression:

- `compress_model.py` - Compress/decompress models with gzip
- `model_optimization.py` - Advanced optimization techniques

### Available compression methods:

1. **Gzip compression** (current): ~7% size reduction
2. **7-Zip compression**: Potentially 15-25% better compression
3. **Model quantization**: Convert to TensorFlow Lite for significant size reduction
4. **External hosting**: Host models on cloud services

## File Size Summary

| File | Original Size | Compressed Size | Compression Ratio |
|------|---------------|-----------------|-------------------|
| `model_phase1.h5` | 152.03 MB | 141.62 MB (gzip) | 6.8% |
| `best_model.h5` | 12.84 MB | N/A (small enough) | - |

## Alternative Solutions

If you're still having issues with file sizes:

1. **GitHub Releases** - Supports files up to 2GB
2. **External hosting** - Google Drive, Dropbox, AWS S3
3. **Hugging Face Model Hub** - Specialized for ML models
4. **Model quantization** - Reduce model precision for smaller size