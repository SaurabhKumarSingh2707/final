#!/usr/bin/env python3
"""
Browser-Triggered Flask Manager
A lightweight HTTP server that can start/stop Flask services from web requests
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class FlaskServiceHandler(BaseHTTPRequestHandler):
    """HTTP handler for Flask service management requests"""
    
    def __init__(self, *args, flask_manager=None, **kwargs):
        self.flask_manager = flask_manager
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/status':
            self.handle_status_request()
        elif parsed_url.path == '/start':
            self.handle_start_request()
        elif parsed_url.path == '/stop':
            self.handle_stop_request()
        elif parsed_url.path == '/health':
            self.handle_health_request()
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/service':
            self.handle_service_request()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_status_request(self):
        """Handle Flask service status request"""
        try:
            status = self.flask_manager.get_flask_status()
            self.send_json_response(status)
        except Exception as e:
            self.send_error_response(f"Error checking status: {e}")
    
    def handle_start_request(self):
        """Handle Flask service start request"""
        try:
            result = self.flask_manager.start_flask_service()
            if result:
                self.send_json_response({
                    "success": True,
                    "message": "Flask service started successfully",
                    "url": "http://127.0.0.1:5000"
                })
            else:
                self.send_json_response({
                    "success": False,
                    "message": "Failed to start Flask service"
                })
        except Exception as e:
            self.send_error_response(f"Error starting service: {e}")
    
    def handle_stop_request(self):
        """Handle Flask service stop request"""
        try:
            result = self.flask_manager.stop_flask_service()
            self.send_json_response({
                "success": result,
                "message": "Flask service stopped" if result else "Failed to stop Flask service"
            })
        except Exception as e:
            self.send_error_response(f"Error stopping service: {e}")
    
    def handle_health_request(self):
        """Handle health check request"""
        self.send_json_response({
            "status": "healthy",
            "service": "KrishiVaani Flask Manager",
            "timestamp": time.time()
        })
    
    def handle_service_request(self):
        """Handle complex service management requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                action = data.get('action', '')
                
                if action == 'start':
                    result = self.flask_manager.start_flask_service()
                elif action == 'stop':
                    result = self.flask_manager.stop_flask_service()
                elif action == 'restart':
                    result = self.flask_manager.restart_flask_service()
                elif action == 'status':
                    result = self.flask_manager.get_flask_status()
                else:
                    self.send_error_response("Invalid action")
                    return
                
                self.send_json_response(result)
            else:
                self.send_error_response("No data provided")
                
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON data")
        except Exception as e:
            self.send_error_response(f"Error processing request: {e}")
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_data = json.dumps(data, indent=2)
        self.wfile.write(response_data.encode('utf-8'))
    
    def send_error_response(self, message):
        """Send error response"""
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = json.dumps({
            "success": False,
            "error": message,
            "timestamp": time.time()
        })
        self.wfile.write(error_data.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override log message to reduce noise"""
        if self.path != '/health':  # Don't log health checks
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

class BrowserTriggeredFlaskManager:
    """Manager class for handling Flask service from browser requests"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.crop_disease_dir = self.base_dir / "crop-disease"
        self.flask_starter_path = self.crop_disease_dir / "flask_auto_starter.py"
        self.server = None
        self.server_thread = None
        
    def get_flask_status(self):
        """Get Flask service status"""
        try:
            if not self.flask_starter_path.exists():
                return {
                    "running": False,
                    "error": "Flask auto starter not found",
                    "url": None
                }
            
            cmd = [sys.executable, str(self.flask_starter_path), "status"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.crop_disease_dir))
            
            is_running = "RUNNING" in result.stdout
            
            return {
                "running": is_running,
                "status": result.stdout.strip(),
                "url": "http://127.0.0.1:5000" if is_running else None,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "running": False,
                "error": f"Error checking status: {e}",
                "url": None
            }
    
    def start_flask_service(self):
        """Start Flask service"""
        try:
            if not self.flask_starter_path.exists():
                return False
            
            cmd = [sys.executable, str(self.flask_starter_path), "start"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.crop_disease_dir))
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error starting Flask service: {e}")
            return False
    
    def stop_flask_service(self):
        """Stop Flask service"""
        try:
            if not self.flask_starter_path.exists():
                return False
            
            cmd = [sys.executable, str(self.flask_starter_path), "stop"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.crop_disease_dir))
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error stopping Flask service: {e}")
            return False
    
    def restart_flask_service(self):
        """Restart Flask service"""
        try:
            self.stop_flask_service()
            time.sleep(2)
            return self.start_flask_service()
        except Exception as e:
            print(f"Error restarting Flask service: {e}")
            return False
    
    def start_http_server(self, port=8765):
        """Start the HTTP server for browser communication"""
        try:
            def handler(*args, **kwargs):
                FlaskServiceHandler(*args, flask_manager=self, **kwargs)
            
            self.server = HTTPServer(('127.0.0.1', port), handler)
            
            print(f"Starting Flask Service Manager on http://127.0.0.1:{port}")
            print("Available endpoints:")
            print(f"  GET  /status  - Check Flask service status")
            print(f"  GET  /start   - Start Flask service")
            print(f"  GET  /stop    - Stop Flask service") 
            print(f"  GET  /health  - Health check")
            print(f"  POST /service - Complex service operations")
            print()
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\nShutting down Flask Service Manager...")
            self.shutdown_server()
        except Exception as e:
            print(f"Error starting HTTP server: {e}")
    
    def start_server_thread(self, port=8765):
        """Start HTTP server in background thread"""
        self.server_thread = threading.Thread(
            target=self.start_http_server, 
            args=(port,),
            daemon=True
        )
        self.server_thread.start()
        time.sleep(1)  # Give server time to start
        return self.server_thread.is_alive()
    
    def shutdown_server(self):
        """Shutdown the HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=5)
            self.server_thread = None

def main():
    """Main entry point"""
    manager = BrowserTriggeredFlaskManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
        
        if command == "start":
            manager.start_http_server(port)
        elif command == "status":
            status = manager.get_flask_status()
            print(json.dumps(status, indent=2))
        elif command == "flask-start":
            result = manager.start_flask_service()
            print("Flask service started:" if result else "Failed to start Flask service")
        elif command == "flask-stop":
            result = manager.stop_flask_service()
            print("Flask service stopped" if result else "Failed to stop Flask service")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: start, status, flask-start, flask-stop")
    else:
        print("Browser-Triggered Flask Manager")
        print("Usage:")
        print("  python browser_flask_manager.py start [port]     - Start HTTP service manager")
        print("  python browser_flask_manager.py status          - Check Flask status")
        print("  python browser_flask_manager.py flask-start     - Start Flask service")
        print("  python browser_flask_manager.py flask-stop      - Stop Flask service")
        print()
        print("Default port: 8765")
        print("Default action: start")
        
        # Start with default settings
        manager.start_http_server()

if __name__ == "__main__":
    main()