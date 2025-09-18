"""
KrishiVaani Smart Crop Based Analysis - Flask App with ML Integration
"""

from flask import Flask, render_template, request, jsonify, send_file
from crop_soil_data import CROP_REQUIREMENTS, FERTILIZER_DETAILS
from pdf_generator import CropReportGenerator
import joblib
import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Load the trained ML model
def load_ml_model():
    """Load the trained machine learning model and related components"""
    try:
        if not os.path.exists('models/crop_recommendation_model.pkl'):
            print("⚠️  ML model not found. Please run train_model.py first.")
            return None, None, None
            
        # Load the model
        model = joblib.load('models/crop_recommendation_model.pkl')
        
        # Load feature columns
        with open('models/feature_columns.pkl', 'rb') as f:
            feature_columns = pickle.load(f)
            
        # Load crop labels
        with open('models/crop_labels.pkl', 'rb') as f:
            crop_labels = pickle.load(f)
            
        print("✅ ML model loaded successfully!")
        return model, feature_columns, crop_labels
        
    except Exception as e:
        print(f"❌ Error loading ML model: {str(e)}")
        return None, None, None

# Load the model at startup (with error handling)
try:
    ML_MODEL, FEATURE_COLUMNS, CROP_LABELS = load_ml_model()
except Exception as e:
    print(f"⚠️  Warning: ML model could not be loaded: {str(e)}")
    print("🔄 App will run without AI prediction features")
    ML_MODEL, FEATURE_COLUMNS, CROP_LABELS = None, None, None

# Initialize PDF generator
pdf_generator = CropReportGenerator()

@app.route('/')
def crop_selection_page():
    """Direct crop selection page."""
    return render_template('crop_selection.html')

@app.route('/api/crop-soil-analysis', methods=['POST'])
def crop_soil_analysis():
    """API endpoint for crop analysis."""
    try:
        data = request.get_json()
        crop_name = data.get('crop', '').lower()
        
        if not crop_name or crop_name not in CROP_REQUIREMENTS:
            return jsonify({'error': 'Invalid crop selection'}), 400
        
        crop_data = CROP_REQUIREMENTS[crop_name]
        fertilizer_recommendations = []
        
        for fert_name in crop_data['recommended_fertilizers']:
            if fert_name in FERTILIZER_DETAILS:
                fertilizer_recommendations.append({
                    'name': fert_name,
                    'details': FERTILIZER_DETAILS[fert_name]
                })
        
        return jsonify({
            'success': True,
            'crop': crop_name.title(),
            'soil_requirements': crop_data['soil_parameters'],
            'fertilizer_recommendations': fertilizer_recommendations,
            'fertilizer_schedule': crop_data['fertilizer_schedule'],
            'recommended_soil_types': crop_data['soil_type'],
            'growing_season': crop_data['season'],
            'growth_duration': crop_data['growth_duration'],
            'indian_locations': crop_data.get('indian_locations', {
                'message': 'Location data not available for this crop'
            })
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/soil-to-crop-prediction', methods=['POST'])
def soil_to_crop_prediction():
    """API endpoint for ML-based crop prediction from soil parameters."""
    try:
        if ML_MODEL is None:
            return jsonify({'error': 'ML model not available. Please train the model first.'}), 500
            
        data = request.get_json()
        
        # Extract soil parameters
        required_params = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        soil_params = {}
        
        for param in required_params:
            if param not in data:
                return jsonify({'error': f'Missing parameter: {param}'}), 400
            try:
                soil_params[param] = float(data[param])
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid value for {param}. Must be a number.'}), 400
        
        # Create input DataFrame
        input_data = pd.DataFrame([soil_params], columns=FEATURE_COLUMNS)
        
        # Make prediction
        prediction = ML_MODEL.predict(input_data)[0]
        probabilities = ML_MODEL.predict_proba(input_data)[0]
        
        # Get top 5 recommendations with probabilities
        top_indices = np.argsort(probabilities)[-5:][::-1]
        recommendations = []
        
        for idx in top_indices:
            crop = ML_MODEL.classes_[idx]
            probability = probabilities[idx]
            confidence = f"{probability * 100:.1f}%"
            
            # Get crop details if available
            crop_details = None
            if crop in CROP_REQUIREMENTS:
                crop_details = {
                    'soil_requirements': CROP_REQUIREMENTS[crop]['soil_parameters'],
                    'growing_season': CROP_REQUIREMENTS[crop]['season'],
                    'growth_duration': CROP_REQUIREMENTS[crop]['growth_duration']
                }
            
            recommendations.append({
                'crop': crop.title(),
                'confidence': confidence,
                'probability': probability,
                'details': crop_details
            })
        
        return jsonify({
            'success': True,
            'input_parameters': soil_params,
            'best_crop': prediction.title(),
            'recommendations': recommendations,
            'model_info': {
                'total_crops': len(ML_MODEL.classes_),
                'feature_importance': dict(zip(FEATURE_COLUMNS, ML_MODEL.feature_importances_))
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crop-list')
def get_crop_list():
    """Get list of available crops for dropdown"""
    crops = list(CROP_REQUIREMENTS.keys())
    return jsonify({'crops': [crop.title() for crop in sorted(crops)]})

@app.route('/api/generate-crop-report', methods=['POST'])
def generate_crop_report():
    """Generate PDF report for crop analysis"""
    try:
        print("🔍 PDF report request received")
        data = request.get_json()
        crop_name = data.get('crop', '').lower()
        print(f"🔍 Crop name: {crop_name}")
        
        if not crop_name or crop_name not in CROP_REQUIREMENTS:
            print(f"❌ Invalid crop: {crop_name}")
            return jsonify({'error': 'Invalid crop selection'}), 400
        
        crop_data = CROP_REQUIREMENTS[crop_name]
        fertilizer_recommendations = []
        
        for fert_name in crop_data['recommended_fertilizers']:
            if fert_name in FERTILIZER_DETAILS:
                fertilizer_recommendations.append({
                    'name': fert_name,
                    'details': FERTILIZER_DETAILS[fert_name]
                })
        
        # Prepare data for PDF generation
        pdf_data = {
            'crop': crop_name.title(),
            'soil_requirements': crop_data['soil_parameters'],
            'fertilizer_recommendations': fertilizer_recommendations,
            'fertilizer_schedule': crop_data['fertilizer_schedule'],
            'recommended_soil_types': crop_data['soil_type'],
            'growing_season': crop_data['season'],
            'growth_duration': crop_data['growth_duration'],
            'indian_locations': crop_data.get('indian_locations', {})
        }
        
        # Generate PDF
        print("🔍 Generating PDF...")
        pdf_buffer = pdf_generator.generate_crop_report(pdf_data)
        print("✅ PDF generated successfully")
        
        # Create filename
        filename = f"Crop_Analysis_{crop_name.title()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        print(f"🔍 Filename: {filename}")
        
        # Reset buffer position for send_file
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-ai-report', methods=['POST'])
def generate_ai_report():
    """Generate PDF report for AI predictions"""
    try:
        if ML_MODEL is None:
            return jsonify({'error': 'ML model not available'}), 500
            
        data = request.get_json()
        
        # Extract soil parameters
        required_params = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        soil_params = {}
        
        for param in required_params:
            if param not in data:
                return jsonify({'error': f'Missing parameter: {param}'}), 400
            try:
                soil_params[param] = float(data[param])
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid value for {param}'}), 400
        
        # Make prediction
        input_data = pd.DataFrame([soil_params], columns=FEATURE_COLUMNS)
        prediction = ML_MODEL.predict(input_data)[0]
        probabilities = ML_MODEL.predict_proba(input_data)[0]
        
        # Get top 5 recommendations
        top_indices = np.argsort(probabilities)[-5:][::-1]
        recommendations = []
        
        for idx in top_indices:
            crop = ML_MODEL.classes_[idx]
            probability = probabilities[idx]
            confidence = f"{probability * 100:.1f}%"
            
            # Get crop details if available
            crop_details = None
            if crop in CROP_REQUIREMENTS:
                crop_details = {
                    'soil_requirements': CROP_REQUIREMENTS[crop]['soil_parameters'],
                    'growing_season': CROP_REQUIREMENTS[crop]['season'],
                    'growth_duration': CROP_REQUIREMENTS[crop]['growth_duration']
                }
            
            recommendations.append({
                'crop': crop.title(),
                'confidence': confidence,
                'probability': probability,
                'details': crop_details
            })
        
        # Prepare data for PDF generation
        pdf_data = {
            'input_parameters': soil_params,
            'best_crop': prediction.title(),
            'recommendations': recommendations
        }
        
        # Generate PDF
        pdf_buffer = pdf_generator.generate_ai_prediction_report(pdf_data)
        
        # Create filename
        filename = f"AI_Crop_Predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Reset buffer position for send_file
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌱 Starting KrishiVaani Smart Crop Based Analysis - Direct to crop selection!")
    app.run(debug=True, host='0.0.0.0', port=5001)