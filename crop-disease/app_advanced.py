"""
KrishiVannai AI Plant Disease Prediction System
Advanced Flask web application for AI-powered plant disease detection
"""

from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import numpy as np
from PIL import Image
import io
import base64
from predict_advanced import AdvancedPlantDiseasePredictor
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'krishivannai-ai-plant-disease-prediction-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

# Global error handler to ensure JSON responses
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected exceptions and return JSON response"""
    logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
    return jsonify({
        'success': False,
        'error': f'Internal server error: {str(e)}'
    }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    if request.path.startswith('/api/') or request.path in ['/predict', '/batch_predict']:
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    return render_template('404.html'), 404

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the advanced predictor
predictor = None

def initialize_predictor():
    """Initialize predictor with better error handling"""
    global predictor
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Check if model files exist with absolute paths
        best_model_path = os.path.join(script_dir, 'best_model.h5')
        model_phase1_path = os.path.join(script_dir, 'model_phase1.h5')
        
        if not os.path.exists(best_model_path) and not os.path.exists(model_phase1_path):
            logger.error("No model files found. Please ensure model files are available.")
            return False
        
        # Initialize with absolute file paths (will fallback to available files)
        predictor = AdvancedPlantDiseasePredictor(
            model_path=os.path.join(script_dir, 'best_model_advanced.h5'),
            class_names_path=os.path.join(script_dir, 'class_names_advanced.txt'),
            fallback_model=os.path.join(script_dir, 'best_model.h5')
        )
        logger.info("✅ Advanced predictor initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize advanced predictor: {e}")
        logger.error(traceback.format_exc())
        return False

# Try to initialize predictor
initialize_predictor()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_uploaded_image(file):
    """
    Process uploaded image and convert to format suitable for prediction
    
    Args:
        file: Uploaded file object
        
    Returns:
        tuple: (processed_image_array, original_image_base64, image_info)
    """
    try:
        # Read image
        image = Image.open(file.stream)
        
        # Get image info
        image_info = {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'filename': file.filename
        }
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save original image as base64 for display
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=95)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        original_image_b64 = f"data:image/jpeg;base64,{img_str}"
        
        # Resize for prediction based on model type
        target_size = (predictor.IMG_WIDTH, predictor.IMG_HEIGHT) if predictor else (224, 224)
        resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
        image_array = np.array(resized_image)
        image_array = image_array.astype('float32') / 255.0
        
        return image_array, original_image_b64, image_info
    
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        raise

@app.route('/')
def index():
    """Enhanced home page"""
    model_info = predictor.get_model_info() if predictor else {'model_type': 'unavailable'}
    return render_template('index_advanced.html', model_info=model_info)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and advanced prediction"""
    try:
        # Check if predictor is available
        if not predictor:
            logger.error("Predictor not available - attempting to reinitialize")
            if not initialize_predictor():
                return jsonify({
                    'success': False,
                    'error': 'Prediction service unavailable. Model not loaded.'
                }), 503
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, TIFF, or WebP files.'
            }), 400
        
        # Get prediction options from form
        use_tta = request.form.get('use_tta', 'true').lower() == 'true'
        enhance_image = request.form.get('enhance_image', 'true').lower() == 'true'
        top_n = min(int(request.form.get('top_n', 5)), 10)  # Max 10 predictions
        
        # Process image
        try:
            image_array, original_image_b64, image_info = process_uploaded_image(file)
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return jsonify({
                'success': False,
                'error': f'Error processing image: {str(e)}'
            }), 400
        
        # Make prediction
        try:
            results = predictor.predict_image_from_array(
                image_array, 
                top_n=top_n, 
                use_tta=use_tta
            )
            
            # Add image and processing info to results
            results['original_image'] = original_image_b64
            results['image_info'] = image_info
            results['processing_options'] = {
                'use_tta': use_tta,
                'enhance_image': enhance_image,
                'top_n': top_n
            }
            
            return jsonify({
                'success': True,
                'results': results
            })
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return jsonify({
                'success': False,
                'error': f'Error making prediction: {str(e)}'
            }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in predict: {e}")
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Handle batch prediction for multiple images"""
    try:
        if not predictor:
            return jsonify({'error': 'Prediction service unavailable'}), 503
        
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'error': 'No files uploaded'}), 400
        
        if len(files) > 10:  # Limit batch size
            return jsonify({'error': 'Maximum 10 files allowed in batch mode'}), 400
        
        results = []
        use_tta = request.form.get('use_tta', 'false').lower() == 'true'  # Disabled by default for batch
        
        for file in files:
            if file.filename == '' or not allowed_file(file.filename):
                continue
            
            try:
                image_array, original_image_b64, image_info = process_uploaded_image(file)
                prediction = predictor.predict_image_from_array(image_array, top_n=3, use_tta=use_tta)
                
                prediction['original_image'] = original_image_b64
                prediction['image_info'] = image_info
                results.append(prediction)
                
            except Exception as e:
                results.append({
                    'error': f'Failed to process {file.filename}: {str(e)}',
                    'filename': file.filename
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'processed_count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': f'Batch prediction failed: {str(e)}'}), 500

@app.route('/model_info')
def model_info():
    """Get detailed model information"""
    if not predictor:
        return jsonify({'error': 'Predictor not available'}), 503
    
    info = predictor.get_model_info()
    info['classes'] = predictor.class_names[:10]  # First 10 classes
    info['total_classes'] = len(predictor.class_names)
    
    return jsonify(info)

@app.route('/health')
def health_check():
    """Enhanced health check endpoint"""
    health_status = {
        'status': 'healthy' if predictor else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'predictor_available': predictor is not None,
        'model_loaded': predictor.model is not None if predictor else False,
        'classes_loaded': len(predictor.class_names) if predictor else 0,
        'model_type': predictor.model_type if predictor else 'none',
        'supports_tta': predictor.model_type == 'advanced' if predictor else False
    }
    
    status_code = 200 if predictor else 503
    return jsonify(health_status), status_code

@app.route('/about')
def about():
    """About page with model and system information"""
    return render_template('about.html', model_info=predictor.get_model_info() if predictor else {})

if __name__ == '__main__':
    print("🚀 Starting KrishiVannai AI Plant Disease Prediction App...")
    
    # Decompress model if needed
    if os.path.exists('model_phase1.h5.gz') and not os.path.exists('model_phase1.h5'):
        print("📦 Decompressing model file...")
        try:
            import gzip
            import shutil
            with gzip.open('model_phase1.h5.gz', 'rb') as f_in:
                with open('model_phase1.h5', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print("✅ Model decompressed successfully")
            # Reinitialize predictor after decompression
            initialize_predictor()
        except Exception as e:
            print(f"❌ Failed to decompress model: {e}")
    
    if predictor:
        model_info = predictor.get_model_info()
        print(f"📊 Model Type: {model_info['model_type']}")
        print(f"🧠 Model Path: {model_info['model_path']}")
        print(f"📐 Input Size: {model_info['input_size']}")
        print(f"🎯 Classes: {model_info['num_classes']}")
        print(f"🔬 TTA Support: {model_info['supports_tta']}")
    else:
        print("⚠️ Predictor not available - check model files")
    
    # Use environment variable for port (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🌐 Starting server on port {port}")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)