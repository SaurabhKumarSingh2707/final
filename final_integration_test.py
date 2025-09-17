#!/usr/bin/env python3
"""
Final Integration Test for KrishiVaani Disease Prediction
Tests all components to ensure everything is working properly.
"""

import requests
import socket
import webbrowser
from pathlib import Path
import time

def test_flask_service():
    """Test if Flask service is running and accessible"""
    print("🧪 Testing Flask Disease Prediction Service...")
    
    try:
        response = requests.get('http://127.0.0.1:5000', timeout=10)
        if response.status_code == 200:
            print("✅ Flask service is running and accessible!")
            print(f"📊 Response status: {response.status_code}")
            return True
        else:
            print(f"⚠️ Flask service responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask service is not running or not accessible")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Flask service is running but slow to respond")
        return False
    except Exception as e:
        print(f"❌ Error testing Flask service: {e}")
        return False

def test_port_availability():
    """Test if port 5000 is in use"""
    print("\n🔌 Testing port availability...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', 5000))
            if result == 0:
                print("✅ Port 5000 is in use (service is running)")
                return True
            else:
                print("❌ Port 5000 is available (service not running)")
                return False
    except Exception as e:
        print(f"❌ Error testing port: {e}")
        return False

def test_files_exist():
    """Test if all integration files exist"""
    print("\n📁 Testing file availability...")
    
    current_dir = Path(__file__).parent
    files_to_check = [
        "simple_flask_launcher.py",
        "Start_Disease_Prediction.bat", 
        "service_manager_gui.py",
        "disease_prediction_launcher.html",
        "README_Disease_Integration.md",
        "crop-disease/app_advanced.py"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_dashboard_integration():
    """Test if dashboard files are properly updated"""
    print("\n🌐 Testing dashboard integration...")
    
    dashboard_file = Path(__file__).parent / "dashboard.html"
    if not dashboard_file.exists():
        print("❌ dashboard.html not found")
        return False
    
    dashboard_content = dashboard_file.read_text(encoding='utf-8')
    
    # Check for our launcher link
    if "disease_prediction_launcher.html" in dashboard_content:
        print("✅ Dashboard links updated to use launcher page")
        return True
    else:
        print("⚠️ Dashboard may not be properly updated")
        return False

def open_test_browser():
    """Open browser for manual testing"""
    print("\n🌐 Opening browser for manual testing...")
    
    try:
        launcher_file = Path(__file__).parent / "disease_prediction_launcher.html"
        if launcher_file.exists():
            file_url = f"file:///{launcher_file.absolute()}"
            webbrowser.open(file_url)
            print(f"✅ Opened launcher page: {file_url}")
            return True
        else:
            print("❌ Launcher page not found")
            return False
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 KrishiVaani Disease Prediction Integration Test")
    print("=" * 60)
    
    results = {
        "Flask Service": test_flask_service(),
        "Port Check": test_port_availability(), 
        "Files": test_files_exist(),
        "Dashboard": test_dashboard_integration()
    }
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Integration is successful!")
        print("\n🚀 Ready to use:")
        print("   1. Open dashboard.html")
        print("   2. Click 'Advanced Disease Prediction'")
        print("   3. Upload plant images for disease detection")
        
        # Open browser for manual verification
        if input("\n🌐 Open launcher page for testing? (y/n): ").lower().startswith('y'):
            open_test_browser()
            print("\n💡 Try uploading a plant image to test the AI!")
            
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed.")
        print("\n🔧 Troubleshooting:")
        
        if not results["Flask Service"]:
            print("   • Run: python simple_flask_launcher.py")
            print("   • Or double-click: Start_Disease_Prediction.bat")
            
        if not results["Files"]:
            print("   • Ensure all integration files are present")
            
        if not results["Dashboard"]:
            print("   • Check dashboard.html for proper link updates")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()