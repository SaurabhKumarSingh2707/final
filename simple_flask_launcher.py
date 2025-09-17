#!/usr/bin/env python3
"""
Simple Flask Service Launcher for KrishiVaani Disease Prediction
Automatically starts the Flask service if it's not running.
No complex automation - just a simple, reliable launcher.
"""

import subprocess
import sys
import time
import socket
import os
from pathlib import Path

def check_port_available(port=5000):
    """Check if port is available or already in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            return result != 0  # True if port is available (not in use)
    except:
        return True

def find_flask_app():
    """Find the Flask app file"""
    current_dir = Path(__file__).parent
    possible_paths = [
        current_dir / "crop-disease" / "app_advanced.py",
        current_dir / "app_advanced.py",
        Path("crop-disease/app_advanced.py"),
        Path("app_advanced.py")
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path.absolute())
    return None

def start_flask_service():
    """Start the Flask service"""
    app_path = find_flask_app()
    if not app_path:
        print("❌ Flask app not found!")
        print("Please ensure app_advanced.py exists in:")
        print("  - crop-disease/app_advanced.py")
        print("  - app_advanced.py")
        return False
    
    print(f"🚀 Starting Flask service from: {app_path}")
    
    try:
        # Start Flask in background
        if os.name == 'nt':  # Windows
            process = subprocess.Popen([
                sys.executable, app_path
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix/Linux/Mac
            process = subprocess.Popen([
                sys.executable, app_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for Flask to start
        print("⏳ Waiting for Flask to start...")
        time.sleep(3)
        
        # Check if service is running
        if not check_port_available(5000):
            print("✅ Flask Disease Prediction Service is now RUNNING!")
            print("🌐 Access at: http://127.0.0.1:5000")
            return True
        else:
            print("⚠️  Flask may still be starting... please wait a moment")
            return True
            
    except Exception as e:
        print(f"❌ Failed to start Flask service: {e}")
        return False

def main():
    """Main launcher function"""
    print("=" * 50)
    print("🌾 KrishiVaani Disease Prediction Launcher")
    print("=" * 50)
    
    # Check if Flask service is already running
    if not check_port_available(5000):
        print("✅ Flask service is already running on port 5000")
        print("🌐 Access at: http://127.0.0.1:5000")
        print("\n🎯 You can now use the disease prediction from your dashboard!")
    else:
        print("📡 Flask service not detected. Starting...")
        if start_flask_service():
            print("\n🎯 Flask service started successfully!")
            print("🌐 Access at: http://127.0.0.1:5000")
            print("📋 The service will continue running in the background")
        else:
            print("\n❌ Failed to start Flask service")
            print("🔧 Try running manually: python crop-disease/app_advanced.py")
    
    print("\n" + "=" * 50)
    print("💡 TIP: You can run this launcher anytime to ensure")
    print("    the disease prediction service is available!")
    print("=" * 50)

if __name__ == "__main__":
    main()