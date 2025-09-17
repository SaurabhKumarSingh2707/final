"""
Vercel serverless function for model information
Returns detailed information about the loaded ML model
"""
import json
from _utils import json_response, error_response, success_response, handle_cors, get_predictor

def handler(event, context):
    """Main handler for model info endpoint"""
    
    # Handle CORS preflight
    cors_response = handle_cors(event)
    if cors_response:
        return cors_response
    
    # Allow GET requests
    if event.get('httpMethod') not in ['GET', 'POST']:
        return error_response('Method not allowed', 405)
    
    try:
        # Get predictor instance
        predictor, error = get_predictor()
        if error:
            return error_response(f'Predictor not available: {error}', 503)
        
        # Get model information
        info = predictor.get_model_info()
        
        # Add additional information
        info['classes_preview'] = predictor.class_names[:10] if hasattr(predictor, 'class_names') else []
        info['total_classes'] = len(predictor.class_names) if hasattr(predictor, 'class_names') else 0
        info['api_version'] = '1.0'
        info['deployment'] = 'vercel-serverless'
        
        return success_response(info)
        
    except Exception as e:
        return error_response(f'Error getting model info: {str(e)}', 500)

# For local testing
if __name__ == '__main__':
    test_event = {
        'httpMethod': 'GET'
    }
    print(handler(test_event, {}))