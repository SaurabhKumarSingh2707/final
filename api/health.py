"""
Vercel serverless function for health check
Returns system status and model availability
"""
import json
from datetime import datetime
from _utils import json_response, error_response, success_response, handle_cors, get_predictor

def handler(event, context):
    """Main handler for health check endpoint"""
    
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
        
        # Build health status
        health_status = {
            'status': 'healthy' if predictor else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'predictor_available': predictor is not None,
            'model_loaded': predictor.model is not None if predictor else False,
            'classes_loaded': len(predictor.class_names) if predictor and hasattr(predictor, 'class_names') else 0,
            'model_type': predictor.model_type if predictor else 'none',
            'supports_tta': predictor.model_type == 'advanced' if predictor else False,
            'deployment': 'vercel-serverless',
            'api_version': '1.0'
        }
        
        if error:
            health_status['error'] = error
        
        # Return appropriate status code
        status_code = 200 if predictor else 503
        
        return json_response({
            'success': predictor is not None,
            'data': health_status,
            'timestamp': datetime.now().isoformat()
        }, status_code)
        
    except Exception as e:
        return error_response(f'Health check failed: {str(e)}', 500)

# For local testing
if __name__ == '__main__':
    test_event = {
        'httpMethod': 'GET'
    }
    print(handler(test_event, {}))