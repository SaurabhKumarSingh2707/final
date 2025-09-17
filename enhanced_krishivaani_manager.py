#!/usr/bin/env python3
"""
Enhanced KrishiVaani Startup Manager
Complete automation system with browser integration
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess
from pathlib import Path

class EnhancedKrishiVaaniManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.crop_disease_dir = self.base_dir / "crop-disease"
        self.flask_starter_path = self.crop_disease_dir / "flask_auto_starter.py"
        self.browser_manager_path = self.base_dir / "browser_flask_manager.py"
        
        self.http_manager_process = None
        self.flask_service_process = None
        
    def start_http_manager(self, port=8765):
        """Start the HTTP service manager in background"""
        try:
            print(f"Starting HTTP Service Manager on port {port}...")
            
            cmd = [sys.executable, str(self.browser_manager_path), "start", str(port)]
            self.http_manager_process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Give it time to start
            time.sleep(2)
            
            if self.http_manager_process.poll() is None:
                print(f"HTTP Service Manager started successfully on http://127.0.0.1:{port}")
                return True
            else:
                print("Failed to start HTTP Service Manager")
                return False
                
        except Exception as e:
            print(f"Error starting HTTP Service Manager: {e}")
            return False
    
    def start_flask_service(self):
        """Start the Flask disease prediction service"""
        try:
            print("Starting Flask Disease Prediction Service...")
            
            if not self.flask_starter_path.exists():
                print("Flask auto starter not found!")
                return False
            
            cmd = [sys.executable, str(self.flask_starter_path), "start"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.crop_disease_dir))
            
            if result.returncode == 0:
                print("Flask service started successfully!")
                print("Service available at: http://127.0.0.1:5000")
                return True
            else:
                print(f"Failed to start Flask service: {result.stderr}")
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
        """Open the KrishiVaani application"""
        try:
            index_path = self.base_dir / "index.html"
            if index_path.exists():
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
    
    def run_complete_startup(self):
        """Run the complete enhanced startup sequence"""
        print("=" * 60)
        print("🚀 KrishiVaani Enhanced Startup System")
        print("=" * 60)
        
        # Step 1: Start HTTP Service Manager
        print("\nStep 1: Starting HTTP Service Manager...")
        http_started = self.start_http_manager()
        
        # Step 2: Start Flask Service
        print("\nStep 2: Starting Flask Disease Prediction Service...")  
        flask_started = self.start_flask_service()
        
        # Step 3: Wait for services to initialize
        print("\nStep 3: Initializing services...")
        time.sleep(3)
        
        # Step 4: Verify services
        print("\nStep 4: Verifying service status...")
        flask_running = self.check_flask_service()
        
        if flask_running:
            print("✅ Flask Disease Prediction Service: RUNNING")
        else:
            print("⚠️ Flask Disease Prediction Service: NOT RUNNING")
        
        if http_started:
            print("✅ HTTP Service Manager: RUNNING")
        else:
            print("⚠️ HTTP Service Manager: NOT RUNNING")
        
        # Step 5: Open application
        print("\nStep 5: Opening KrishiVaani Application...")
        app_opened = self.open_application()
        
        # Summary
        print("\n" + "=" * 60)
        print("🌾 KrishiVaani Enhanced Startup Complete!")
        print("=" * 60)
        
        print("\n📊 Service Status:")
        if flask_running:
            print("   🤖 AI Disease Prediction: http://127.0.0.1:5000")
        else:
            print("   ⚠️ AI Disease Prediction: Not Running")
            
        if http_started:
            print("   🔗 HTTP Service Manager: http://127.0.0.1:8765")
        else:
            print("   ⚠️ HTTP Service Manager: Not Running")
        
        if app_opened:
            print("   🌐 Main Application: Opened in browser")
        else:
            print("   ⚠️ Main Application: Failed to open")
        
        print("\n🔧 Features:")
        print("   • Automatic Flask service detection")
        print("   • Browser-based service management")
        print("   • Real-time status indicators")
        print("   • One-click disease prediction access")
        
        print("\n💡 Usage:")
        print("   • Click on Plant Disease tab in dashboard")
        print("   • Services will auto-start if needed")
        print("   • Status indicators show service health")
        
        print("\n🛑 To stop all services:")
        print("   python enhanced_krishivaani_manager.py stop")
        
        return {
            'http_manager': http_started,
            'flask_service': flask_running,
            'application': app_opened
        }
    
    def stop_all_services(self):
        """Stop all running services"""
        print("Stopping all KrishiVaani services...")
        
        # Stop Flask service
        try:
            cmd = [sys.executable, str(self.flask_starter_path), "stop"]
            subprocess.run(cmd, cwd=str(self.crop_disease_dir))
            print("Flask service stopped")
        except Exception as e:
            print(f"Error stopping Flask service: {e}")
        
        # Stop HTTP manager
        if self.http_manager_process and self.http_manager_process.poll() is None:
            try:
                self.http_manager_process.terminate()
                self.http_manager_process.wait(timeout=5)
                print("HTTP Service Manager stopped")
            except Exception as e:
                print(f"Error stopping HTTP Service Manager: {e}")
        
        print("All services stopped!")
    
    def get_service_status(self):
        """Get status of all services"""
        flask_running = self.check_flask_service()
        http_running = self.http_manager_process and self.http_manager_process.poll() is None
        
        print("KrishiVaani Service Status:")
        print(f"  Flask Service: {'✅ RUNNING' if flask_running else '❌ STOPPED'}")
        print(f"  HTTP Manager:  {'✅ RUNNING' if http_running else '❌ STOPPED'}")
        
        if flask_running:
            print("  Disease Prediction: http://127.0.0.1:5000")
        if http_running:
            print("  Service Manager: http://127.0.0.1:8765")
        
        return {
            'flask_service': flask_running,
            'http_manager': http_running
        }

def main():
    """Main entry point"""
    manager = EnhancedKrishiVaaniManager()
    
    if len(sys.argv) < 2:
        # Default action: run complete startup
        manager.run_complete_startup()
        
        # Keep HTTP manager running
        try:
            print("\n⏸️ Press Ctrl+C to stop all services...")
            while True:
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            manager.stop_all_services()
        
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        manager.run_complete_startup()
        
        # Keep running
        try:
            print("\n⏸️ Press Ctrl+C to stop all services...")
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            manager.stop_all_services()
            
    elif command == "stop":
        manager.stop_all_services()
        
    elif command == "status":
        manager.get_service_status()
        
    elif command == "flask":
        manager.start_flask_service()
        
    elif command == "http":
        manager.start_http_manager()
        print("Press Ctrl+C to stop...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping HTTP manager...")
            
    elif command == "open":
        manager.open_application()
        
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        print("  start  - Start all services (default)")
        print("  stop   - Stop all services")  
        print("  status - Check service status")
        print("  flask  - Start only Flask service")
        print("  http   - Start only HTTP manager")
        print("  open   - Open application")

if __name__ == "__main__":
    main()