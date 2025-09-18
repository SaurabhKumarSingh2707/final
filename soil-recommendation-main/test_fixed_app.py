#!/usr/bin/env python3
"""
Quick test to verify the fixed web application
"""

import requests
import json
import time

def test_endpoints():
    """Test both API endpoints"""
    print("🧪 Testing Fixed Web Application")
    print("=" * 50)
    
    # Wait for Flask to be ready
    time.sleep(2)
    
    # Test 1: Crop Analysis
    print("\n1️⃣ Testing Crop Analysis API...")
    try:
        response = requests.post(
            'http://127.0.0.1:5001/api/crop-soil-analysis',
            json={'crop': 'rice'},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: {data.get('crop')} analysis complete")
            print(f"   Fertilizers: {len(data.get('fertilizer_recommendations', []))}")
            print(f"   Season: {data.get('growing_season')}")
        else:
            print(f"❌ FAILED: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: Soil Prediction  
    print("\n2️⃣ Testing Soil Prediction API...")
    try:
        soil_data = {
            'N': 90, 'P': 42, 'K': 43, 
            'temperature': 25, 'humidity': 80, 
            'ph': 6.5, 'rainfall': 200
        }
        response = requests.post(
            'http://127.0.0.1:5001/api/soil-to-crop-prediction',
            json=soil_data,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Best crop is {data.get('best_crop')}")
            recs = data.get('recommendations', [])[:3]
            print(f"   Top 3: {', '.join([r['crop'] for r in recs])}")
        else:
            print(f"❌ FAILED: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print(f"\n🎉 Test completed!")

if __name__ == "__main__":
    test_endpoints()