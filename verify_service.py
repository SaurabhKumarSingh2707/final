#!/usr/bin/env python3
"""
KrishiVaani Service Verification Script
Quick check to verify that the disease prediction service is working correctly
"""

import requests
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("🌾 KrishiVaani Disease Prediction Service Verification")
    print("=" * 60)
    
    try:
        print("🔍 Testing Flask service at http://127.0.0.1:5000...")
        
        # Test the service
        response = requests.get('http://127.0.0.1:5000', timeout=10)
        
        if response.status_code == 200:
            print("✅ SUCCESS: Flask service is running and accessible!")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📄 Response Length: {len(response.text)} characters")
            
            # Check if it's the right service
            if "Plant Disease" in response.text or "disease" in response.text.lower():
                print("✅ VERIFIED: This is the disease prediction service!")
            else:
                print("⚠️  WARNING: Service running but may not be the disease prediction app")
            
            print("\n🎯 READY TO USE:")
            print("   1. Open your dashboard")
            print("   2. Click 'Advanced Disease Prediction'")
            print("   3. Upload plant images for AI analysis")
            
        else:
            print(f"❌ ERROR: Service responded with status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Flask service")
        print("\n🔧 TO FIX THIS:")
        print("   1. Double-click 'Start_Disease_Prediction.bat'")
        print("   2. Or run: python simple_flask_launcher.py")
        print("   3. Or run: python crop-disease/app_advanced.py")
        print("   4. Wait 10-15 seconds, then try again")
        
    except requests.exceptions.Timeout:
        print("⏱️ ERROR: Service is taking too long to respond")
        print("   The service might be starting up. Wait a moment and try again.")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        print("   Try restarting the service manually")
    
    print("\n" + "=" * 60)
    print("💡 TIP: Keep this window open to verify service status anytime!")
    print("=" * 60)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")