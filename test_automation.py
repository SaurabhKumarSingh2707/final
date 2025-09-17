#!/usr/bin/env python3
"""
KrishiVaani Automation Test
Verify that all automation components are working correctly
"""

import os
import sys
import time
import requests
from pathlib import Path

def test_flask_service():
    """Test if Flask service is accessible"""
    try:
        response = requests.get('http://127.0.0.1:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Flask Service (127.0.0.1:5000): WORKING")
            return True
        else:
            print(f"❌ Flask Service: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask Service: NOT ACCESSIBLE ({e})")
        return False

def test_http_manager():
    """Test if HTTP Manager is accessible"""
    try:
        response = requests.get('http://127.0.0.1:8765/status', timeout=5)
        if response.status_code == 200:
            print("✅ HTTP Manager (127.0.0.1:8765): WORKING")
            return True
        else:
            print(f"❌ HTTP Manager: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Manager: NOT ACCESSIBLE ({e})")
        return False

def test_start_service_via_manager():
    """Test starting Flask service via HTTP Manager"""
    try:
        response = requests.get('http://127.0.0.1:8765/start', timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ HTTP Manager Start Command: WORKING")
                return True
            else:
                print(f"❌ HTTP Manager Start: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Manager Start: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Manager Start: FAILED ({e})")
        return False

def check_files_exist():
    """Check if all automation files exist"""
    base_dir = Path(__file__).parent.absolute()
    
    files_to_check = [
        'flask-auto-start.js',
        'advanced-flask-auto-starter.js',
        'flask-service-manager.js',
        'enhanced_krishivaani_manager.py',
        'browser_flask_manager.py',
        'krishivaani_manager.py',
        'start_krishivaani.bat',
        'crop-disease/flask_auto_starter.py',
        'crop-disease/app_advanced.py',
        'index.html',
        'dashboard.html'
    ]
    
    missing_files = []
    
    for file_path in files_to_check:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}: EXISTS")
        else:
            print(f"❌ {file_path}: MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def main():
    print("=" * 60)
    print("🧪 KrishiVaani Automation System Test")
    print("=" * 60)
    
    print("\n📁 Checking File Structure...")
    files_ok = check_files_exist()
    
    print("\n🌐 Testing Services...")
    flask_ok = test_flask_service()
    manager_ok = test_http_manager()
    
    print("\n🔧 Testing Service Management...")
    start_ok = test_start_service_via_manager()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    total_tests = 4
    passed_tests = sum([files_ok, flask_ok, manager_ok, start_ok])
    
    print(f"Files Structure: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"Flask Service:   {'✅ PASS' if flask_ok else '❌ FAIL'}")
    print(f"HTTP Manager:    {'✅ PASS' if manager_ok else '❌ FAIL'}")
    print(f"Service Control: {'✅ PASS' if start_ok else '❌ FAIL'}")
    
    print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your KrishiVaani automation system is fully functional!")
        print("\n🚀 How to use:")
        print("   1. Open dashboard.html in your browser")
        print("   2. Click on 'Advanced Disease Prediction'")
        print("   3. Service will auto-start if needed")
        print("   4. Enjoy AI-powered disease prediction!")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed")
        print("Please check the failed components above.")
        
        if not flask_ok or not manager_ok:
            print("\n💡 Quick Fix:")
            print("   Run: python enhanced_krishivaani_manager.py")
    
    print("\n🔗 Service URLs:")
    print("   🤖 Flask Disease Prediction: http://127.0.0.1:5000")
    print("   🔧 HTTP Service Manager: http://127.0.0.1:8765")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)