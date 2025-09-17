"""
Vercel serverless function for disease prediction
Handles single image prediction with advanced AI
"""
import json
import base64
import io
from PIL import Image
import numpy as np
from _utils import json_response, error_response, success_response, handle_cors, get_predictor, allowed_file

def handler(event, context):
    """Main handler for Vercel serverless function"""
    
    # Handle CORS preflight
    cors_response = handle_cors(event)
    if cors_response:
        return cors_response
    
    # Only allow POST requests
    if event.get('httpMethod') != 'POST':
        return error_response('Method not allowed', 405)
    
    try:
        # Get predictor instance
        predictor, error = get_predictor()
        if error:
            return error_response(f'Prediction service unavailable: {error}', 503)
        
        # Parse the request body
        body = event.get('body', '')
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body).decode('utf-8')
        
        # For multipart form data, we need to handle it differently in serverless
        # For now, we'll expect base64 encoded image data in JSON
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            return error_response('Invalid JSON in request body', 400)
        
        # Check if image data is provided
        if 'image' not in request_data:
            return error_response('No image data provided', 400)
        
        image_data = request_data['image']
        
        # Parse options
        use_tta = request_data.get('use_tta', True)
        enhance_image = request_data.get('enhance_image', True)  
        top_n = min(int(request_data.get('top_n', 5)), 10)
        filename = request_data.get('filename', 'uploaded_image.jpg')
        
        # Validate filename
        if not allowed_file(filename):
            return error_response('Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, TIFF, or WebP files.', 400)
        
        # Process base64 image data
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Get image info
            image_info = {
                'format': image.format or 'JPEG',
                'mode': image.mode,
                'size': image.size,
                'filename': filename
            }
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create base64 for display (reuse the processed image)
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='JPEG', quality=95)
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            original_image_b64 = f"data:image/jpeg;base64,{img_str}"
            
            # Resize for prediction
            target_size = (predictor.IMG_WIDTH, predictor.IMG_HEIGHT)
            resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
            image_array = np.array(resized_image)
            image_array = image_array.astype('float32') / 255.0
            
        except Exception as e:
            return error_response(f'Error processing image: {str(e)}', 400)
        
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
            
            return success_response(results)
            
        except Exception as e:
            return error_response(f'Error making prediction: {str(e)}', 500)
    
    except Exception as e:
        return error_response(f'Unexpected error: {str(e)}', 500)

# For local testing
if __name__ == '__main__':
    # Test the function locally
    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'image': 'test_base64_image_data_here',
            'use_tta': True,
            'top_n': 5,
            'filename': 'test.jpg'
        })
    }
    print(handler(test_event, {}))