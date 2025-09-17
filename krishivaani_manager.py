#!/usr/bin/env python3
"""
KrishiVaani Service Manager - Integrated startup script
This script manages all KrishiVaani services inc        if self.check_flask_service():
            print("Services are running")
        else:
            print("Services are not running")
    else:
        print(f"Unknown command: {command}")
        print("Available commands: start, stop, flask, open, status")Flask backend.
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

class KrishiVaaniManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.crop_disease_dir = self.base_dir / "crop-disease"
        self.flask_starter_path = self.crop_disease_dir / "flask_auto_starter.py"
        
    def start_flask_service(self):
        """Start the Flask disease prediction service"""
        try:
            print("Starting KrishiVaani Disease Prediction Service...")
            
            if not self.flask_starter_path.exists():
                print("Flask auto starter not found!")
                return False
            
            # Start Flask service using the auto starter
            cmd = [sys.executable, str(self.flask_starter_path), "start"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.crop_disease_dir))
            
            if result.returncode == 0:
                print("Disease prediction service started successfully!")
                return True
            else:
                print(f"Failed to start service: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error starting Flask service: {e}")
            return False
    
    def check_flask_service(self):
        """Check if Flask service is running"""
        try:
            cmd = [sys.executable, str(self.flask_starter_path), "status"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.crop_disease_dir))
            return "RUNNING" in result.stdout
        except:
            return False
    
    def open_application(self):
        """Open the main KrishiVaani application"""
        try:
            index_path = self.base_dir / "index.html"
            if index_path.exists():
                # Convert to file URL
                file_url = f"file:///{str(index_path).replace(os.sep, '/')}"
                print(f"Opening KrishiVaani at: {file_url}")
                webbrowser.open(file_url)
                return True
            else:
                print("index.html not found!")
                return False
        except Exception as e:
            print(f"Error opening application: {e}")
            return False
    
    def run_integrated_startup(self):
        """Run the complete startup sequence"""
        print("KrishiVaani Integrated Startup")
        print("=" * 50)
        
        # Step 1: Start Flask service
        print("Step 1: Starting backend services...")
        if not self.start_flask_service():
            print("Backend service failed to start, but continuing...")
        
        # Step 2: Wait a moment for services to initialize
        print("Step 2: Initializing services...")
        time.sleep(2)
        
        # Step 3: Check service status
        print("Step 3: Checking service status...")
        if self.check_flask_service():
            print("All backend services are running!")
        else:
            print("Some services may not be running properly")
        
        # Step 4: Open the application
        print("Step 4: Opening KrishiVaani application...")
        if self.open_application():
            print("Application opened successfully!")
        else:
            print("Failed to open application")
        
        print("=" * 50)
        print("KrishiVaani is ready!")
        print("Disease Prediction: http://127.0.0.1:5000")
        print("Main Application: Open in your browser")
        print("To stop services: python krishivaani_manager.py stop")

    def stop_all_services(self):
        """Stop all running services"""
        print("Stopping KrishiVaani services...")
        
        try:
            cmd = [sys.executable, str(self.flask_starter_path), "stop"]
            subprocess.run(cmd, cwd=str(self.crop_disease_dir))
            print("All services stopped!")
        except Exception as e:
            print(f"Error stopping services: {e}")

def main():
    manager = KrishiVaaniManager()
    
    if len(sys.argv) < 2:
        # Default action: run integrated startup
        manager.run_integrated_startup()
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        manager.run_integrated_startup()
    elif command == "stop":
        manager.stop_all_services()
    elif command == "flask":
        manager.start_flask_service()
    elif command == "open":
        manager.open_application()
    elif command == "status":
        if manager.check_flask_service():
            print("✅ Services are running")
        else:
            print("❌ Services are not running")
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: start, stop, flask, open, status")

if __name__ == "__main__":
    main()