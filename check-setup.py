#!/usr/bin/env python3
"""
KrishiVaani Disease Prediction Setup Checker
This script verifies that all components are properly configured.
"""

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Requires Python 3.7+)")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('tensorflow', 'TensorFlow')
    ]
    
    all_installed = True
    
    for package_name, display_name in required_packages:
        try:
            importlib.import_module(package_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} (Not installed)")
            all_installed = False
    
    return all_installed

def check_model_files():
    """Check if model files exist"""
    print("\n🧠 Checking model files...")
    
    model_files = [
        'best_model.h5',
        'class_names.txt',
        'app_advanced.py',
        'predict_advanced.py'
    ]
    
    all_exist = True
    
    for file_name in model_files:
        if os.path.exists(file_name):
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} (Missing)")
            all_exist = False
    
    return all_exist

def check_dashboard_integration():
    """Check if dashboard files are properly integrated"""
    print("\n🌐 Checking dashboard integration...")
    
    dashboard_files = [
        '../dashboard.html',
        '../disease-prediction-integrated.html',
        '../start-disease-server.bat',
        '../start-disease-server.ps1'
    ]
    
    all_exist = True
    
    for file_name in dashboard_files:
        if os.path.exists(file_name):
            print(f"   ✅ {file_name.replace('../', '')}")
        else:
            print(f"   ❌ {file_name.replace('../', '')} (Missing)")
            all_exist = False
    
    return all_exist

def test_flask_import():
    """Test if Flask can be imported and basic app created"""
    print("\n🚀 Testing Flask functionality...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        print("   ✅ Flask app creation successful")
        return True
    except Exception as e:
        print(f"   ❌ Flask test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🌾 KrishiVaani Disease Prediction Setup Checker")
    print("=" * 50)
    
    # Change to crop-disease-clean-main directory if not already there
    if not os.path.exists('app_advanced.py'):
        if os.path.exists('crop-disease-clean-main'):
            os.chdir('crop-disease-clean-main')
            print("📁 Changed to crop-disease-clean-main directory")
        else:
            print("❌ Could not find crop-disease-clean-main directory")
            print("   Please run this script from the correct location")
            return False
    
    checks = [
        check_python_version(),
        check_required_packages(),
        check_model_files(),
        check_dashboard_integration(),
        test_flask_import()
    ]
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if all(checks):
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your setup is ready for disease prediction")
        print("\n🚀 To start the server:")
        print("   • Double-click start-disease-server.bat")
        print("   • Or run: python app_advanced.py")
        return True
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("❌ Please address the issues above before proceeding")
        print("\n🔧 Quick fixes:")
        print("   • Install missing packages: pip install flask pillow numpy tensorflow")
        print("   • Ensure you're in the correct directory")
        print("   • Download missing model files if needed")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)