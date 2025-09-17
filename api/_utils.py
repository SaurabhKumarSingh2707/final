"""
Shared utilities for Vercel serverless functions
"""
import os
import sys
import json
from datetime import datetime

# Add the current directory to Python path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
crop_disease_dir = os.path.join(parent_dir, 'crop-disease')

sys.path.insert(0, parent_dir)
sys.path.insert(0, crop_disease_dir)

def json_response(data, status_code=200):
    """Create a JSON response for Vercel"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(data)
    }

def error_response(message, status_code=500):
    """Create an error response"""
    return json_response({
        'success': False,
        'error': message,
        'timestamp': datetime.now().isoformat()
    }, status_code)

def success_response(data):
    """Create a success response"""
    return json_response({
        'success': True,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })

def handle_cors(event):
    """Handle CORS preflight requests"""
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': ''
        }
    return None

# Global predictor instance (will be loaded lazily)
_predictor = None
_predictor_error = None

def get_predictor():
    """Get or initialize the predictor instance"""
    global _predictor, _predictor_error
    
    if _predictor is not None:
        return _predictor, None
        
    if _predictor_error is not None:
        return None, _predictor_error
    
    try:
        # Import the predictor class
        from predict_advanced import AdvancedPlantDiseasePredictor
        
        # Initialize with model files from crop-disease directory
        model_path = os.path.join(crop_disease_dir, 'best_model_advanced.h5')
        class_names_path = os.path.join(crop_disease_dir, 'class_names_advanced.txt')
        fallback_model = os.path.join(crop_disease_dir, 'best_model.h5')
        
        _predictor = AdvancedPlantDiseasePredictor(
            model_path=model_path,
            class_names_path=class_names_path,
            fallback_model=fallback_model
        )
        
        return _predictor, None
        
    except Exception as e:
        _predictor_error = str(e)
        return None, _predictor_error

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS