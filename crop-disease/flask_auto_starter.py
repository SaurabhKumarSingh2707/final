#!/usr/bin/env python3
"""
Flask Auto Starter - Automatically manages Flask app lifecycle
This script ensures the Flask app runs automatically when needed.
"""

import os
import sys
import subprocess
import psutil
import time
import threading
import signal
from pathlib import Path

class FlaskAutoStarter:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.flask_app_path = self.script_dir / "app_advanced.py"
        self.pid_file = self.script_dir / "flask_app.pid"
        self.log_file = self.script_dir / "flask_app.log"
        self.flask_process = None
        
    def is_flask_running(self):
        """Check if Flask app is already running"""
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # Check if process with this PID exists and is our Flask app
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    if "python" in process.name().lower() and "app_advanced.py" in " ".join(process.cmdline()):
                        return True, pid
                    
            except (ValueError, psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return False, None
    
    def start_flask_app(self):
        """Start the Flask application"""
        try:
            print("Starting Flask disease prediction service...")
            
            # Check if already running
            is_running, pid = self.is_flask_running()
            if is_running:
                print(f"Flask app already running with PID {pid}")
                return True
                
            # Start Flask app as subprocess
            cmd = [sys.executable, str(self.flask_app_path)]
            
            with open(self.log_file, 'w') as log:
                self.flask_process = subprocess.Popen(
                    cmd,
                    cwd=str(self.script_dir),
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
            
            # Save PID for later reference
            with open(self.pid_file, 'w') as f:
                f.write(str(self.flask_process.pid))
                
            # Wait a moment to ensure it started properly
            time.sleep(3)
            
            if self.flask_process.poll() is None:  # Process is still running
                print(f"Flask app started successfully with PID {self.flask_process.pid}")
                print(f"Service available at: http://127.0.0.1:5000")
                print(f"Logs: {self.log_file}")
                return True
            else:
                print("Flask app failed to start")
                return False
                
        except Exception as e:
            print(f"Error starting Flask app: {e}")
            return False
    
    def stop_flask_app(self):
        """Stop the Flask application"""
        try:
            is_running, pid = self.is_flask_running()
            if not is_running:
                print("ℹ️ Flask app is not running")
                return True
                
            # Terminate the process
            process = psutil.Process(pid)
            process.terminate()
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=5)
                print(f"Flask app stopped gracefully (PID {pid})")
            except psutil.TimeoutExpired:
                # Force kill if necessary
                process.kill()
                print(f"Flask app force-killed (PID {pid})")
                
            # Clean up PID file
            if self.pid_file.exists():
                self.pid_file.unlink()
                
            return True
            
        except Exception as e:
            print(f"Error stopping Flask app: {e}")
            return False
    
    def restart_flask_app(self):
        """Restart the Flask application"""
        print("Restarting Flask app...")
        self.stop_flask_app()
        time.sleep(2)
        return self.start_flask_app()
    
    def status(self):
        """Get Flask app status"""
        is_running, pid = self.is_flask_running()
        if is_running:
            try:
                process = psutil.Process(pid)
                cpu_percent = process.cpu_percent()
                memory_info = process.memory_info()
                
                print(f"Flask App Status: RUNNING")
                print(f"PID: {pid}")
                print(f"CPU Usage: {cpu_percent}%")
                print(f"Memory: {memory_info.rss / 1024 / 1024:.1f} MB")
                print(f"URL: http://127.0.0.1:5000")
                
                return True
            except psutil.NoSuchProcess:
                print("Flask App Status: STOPPED (PID file stale)")
                return False
        else:
            print("Flask App Status: STOPPED")
            return False
    
    def run_daemon(self):
        """Run as a daemon that monitors and maintains the Flask app"""
        print("Starting Flask Auto-Starter Daemon...")
        
        def signal_handler(signum, frame):
            print("\nShutting down daemon...")
            self.stop_flask_app()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        while True:
            try:
                is_running, _ = self.is_flask_running()
                if not is_running:
                    print("Flask app not running, starting...")
                    self.start_flask_app()
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                print("\nDaemon interrupted by user")
                break
            except Exception as e:
                print(f"Daemon error: {e}")
                time.sleep(5)
        
        self.stop_flask_app()

def main():
    starter = FlaskAutoStarter()
    
    if len(sys.argv) < 2:
        print("Flask Auto Starter - Disease Prediction Service Manager")
        print("Usage:")
        print("  python flask_auto_starter.py start     - Start Flask app")
        print("  python flask_auto_starter.py stop      - Stop Flask app")
        print("  python flask_auto_starter.py restart   - Restart Flask app")
        print("  python flask_auto_starter.py status    - Check Flask app status")
        print("  python flask_auto_starter.py daemon    - Run as daemon (auto-restart)")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        starter.start_flask_app()
    elif command == "stop":
        starter.stop_flask_app()
    elif command == "restart":
        starter.restart_flask_app()
    elif command == "status":
        starter.status()
    elif command == "daemon":
        starter.run_daemon()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: start, stop, restart, status, daemon")

if __name__ == "__main__":
    main()