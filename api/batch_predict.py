"""
Vercel serverless function for batch disease prediction
Handles multiple images prediction
"""
import json
import base64
import io
from PIL import Image
import numpy as np
from _utils import json_response, error_response, success_response, handle_cors, get_predictor, allowed_file

def handler(event, context):
    """Main handler for batch prediction"""
    
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
        
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            return error_response('Invalid JSON in request body', 400)
        
        # Check if images data is provided
        if 'images' not in request_data or not isinstance(request_data['images'], list):
            return error_response('No images data provided or invalid format', 400)
        
        images_data = request_data['images']
        
        # Limit batch size
        if len(images_data) > 10:
            return error_response('Maximum 10 files allowed in batch mode', 400)
        
        if len(images_data) == 0:
            return error_response('No images provided', 400)
        
        # Parse options
        use_tta = request_data.get('use_tta', False)  # Disabled by default for batch
        
        results = []
        
        for idx, image_item in enumerate(images_data):
            try:
                # Each image item should have 'image' (base64) and 'filename'
                if 'image' not in image_item:
                    results.append({
                        'error': f'No image data provided for item {idx}',
                        'index': idx
                    })
                    continue
                
                image_data = image_item['image']
                filename = image_item.get('filename', f'image_{idx}.jpg')
                
                # Validate filename
                if not allowed_file(filename):
                    results.append({
                        'error': f'Invalid file type for {filename}',
                        'filename': filename,
                        'index': idx
                    })
                    continue
                
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
                    
                    # Create base64 for display (smaller size for batch)
                    display_image = image.resize((150, 150), Image.Resampling.LANCZOS)
                    img_buffer = io.BytesIO()
                    display_image.save(img_buffer, format='JPEG', quality=80)
                    img_str = base64.b64encode(img_buffer.getvalue()).decode()
                    original_image_b64 = f"data:image/jpeg;base64,{img_str}"
                    
                    # Resize for prediction
                    target_size = (predictor.IMG_WIDTH, predictor.IMG_HEIGHT)
                    resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
                    image_array = np.array(resized_image)
                    image_array = image_array.astype('float32') / 255.0
                    
                    # Make prediction
                    prediction = predictor.predict_image_from_array(
                        image_array, 
                        top_n=3,  # Limit to top 3 for batch
                        use_tta=use_tta
                    )
                    
                    prediction['original_image'] = original_image_b64
                    prediction['image_info'] = image_info
                    prediction['index'] = idx
                    results.append(prediction)
                    
                except Exception as e:
                    results.append({
                        'error': f'Failed to process {filename}: {str(e)}',
                        'filename': filename,
                        'index': idx
                    })
                    
            except Exception as e:
                results.append({
                    'error': f'Failed to process item {idx}: {str(e)}',
                    'index': idx
                })
        
        return success_response({
            'results': results,
            'processed_count': len(results),
            'processing_options': {
                'use_tta': use_tta,
                'top_n': 3
            }
        })
        
    except Exception as e:
        return error_response(f'Batch prediction failed: {str(e)}', 500)

# For local testing
if __name__ == '__main__':
    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'images': [
                {
                    'image': 'test_base64_image_data_1',
                    'filename': 'test1.jpg'
                },
                {
                    'image': 'test_base64_image_data_2', 
                    'filename': 'test2.jpg'
                }
            ],
            'use_tta': False
        })
    }
    print(handler(test_event, {}))