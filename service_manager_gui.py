"""
KrishiVaani Service Manager - Simple GUI
A simple GUI application to manage the Flask disease prediction service
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import socket
import threading
import time
from pathlib import Path

class KrishiVaaniServiceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("KrishiVaani Service Manager")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Variables
        self.service_status = tk.StringVar(value="Checking...")
        self.flask_process = None
        
        # Create GUI
        self.create_widgets()
        
        # Start status checking
        self.check_service_status()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
        
    def create_widgets(self):
        """Create the GUI widgets"""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        ttk.Label(title_frame, text="🌾 KrishiVaani", font=("Arial", 16, "bold")).pack()
        ttk.Label(title_frame, text="Disease Prediction Service Manager", font=("Arial", 10)).pack()
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Status Frame
        status_frame = ttk.Frame(self.root, padding="20")
        status_frame.pack(fill=tk.X)
        
        ttk.Label(status_frame, text="Service Status:", font=("Arial", 12, "bold")).pack()
        self.status_label = ttk.Label(status_frame, textvariable=self.service_status, 
                                     font=("Arial", 11))
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(pady=5, fill=tk.X)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(self.root, padding="20")
        buttons_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(buttons_frame, text="🚀 Start Service", 
                                   command=self.start_service, width=20)
        self.start_btn.pack(pady=5)
        
        self.stop_btn = ttk.Button(buttons_frame, text="🛑 Stop Service", 
                                  command=self.stop_service, width=20)
        self.stop_btn.pack(pady=5)
        
        self.refresh_btn = ttk.Button(buttons_frame, text="🔄 Refresh Status", 
                                     command=self.check_service_status, width=20)
        self.refresh_btn.pack(pady=5)
        
        self.open_btn = ttk.Button(buttons_frame, text="🌐 Open Disease Prediction", 
                                  command=self.open_service, width=20)
        self.open_btn.pack(pady=5)
        
        # Info Frame
        info_frame = ttk.Frame(self.root, padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """
Service URL: http://127.0.0.1:5000
Auto-refresh every 5 seconds
        """
        ttk.Label(info_frame, text=info_text.strip(), font=("Arial", 9), 
                 justify=tk.CENTER, foreground="gray").pack()
        
    def check_port_available(self, port=5000):
        """Check if port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))
                return result != 0
        except:
            return True
            
    def check_service_status(self):
        """Check service status in background thread"""
        def check():
            self.progress.start()
            
            if not self.check_port_available(5000):
                self.service_status.set("✅ Running - http://127.0.0.1:5000")
                self.status_label.config(foreground="green")
                self.start_btn.config(state="disabled")
                self.stop_btn.config(state="normal")
                self.open_btn.config(state="normal")
            else:
                self.service_status.set("❌ Not Running")
                self.status_label.config(foreground="red")
                self.start_btn.config(state="normal")
                self.stop_btn.config(state="disabled")
                self.open_btn.config(state="disabled")
                
            self.progress.stop()
            
            # Schedule next check
            self.root.after(5000, self.check_service_status)
            
        threading.Thread(target=check, daemon=True).start()
        
    def find_flask_app(self):
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
        
    def start_service(self):
        """Start the Flask service"""
        try:
            self.service_status.set("🚀 Starting service...")
            self.status_label.config(foreground="orange")
            self.progress.start()
            
            # Method 1: Try to run Start_Disease_Prediction.bat first
            batch_file_path = Path(__file__).parent / "Start_Disease_Prediction.bat"
            if batch_file_path.exists():
                try:
                    self.service_status.set("🚀 Running Start_Disease_Prediction.bat...")
                    subprocess.Popen([str(batch_file_path)], 
                                   creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0,
                                   shell=True)
                    
                    # Wait a moment for the batch file to start
                    time.sleep(2)
                    
                    # Check if service is now running after batch execution
                    if not self.check_port_available(5000):
                        self.service_status.set("✅ Service started via batch file!")
                        self.root.after(2000, self.verify_start)
                        return
                        
                except Exception as batch_error:
                    print(f"Batch file execution failed: {batch_error}")
            
            # Method 2: Fallback to direct Flask app execution
            app_path = self.find_flask_app()
            if not app_path:
                messagebox.showerror("Error", 
                                   "Flask app not found!\n\n"
                                   "Please ensure app_advanced.py exists in:\n"
                                   "• crop-disease/app_advanced.py\n"
                                   "• app_advanced.py\n\n"
                                   "Also ensure Start_Disease_Prediction.bat exists.")
                self.check_service_status()
                return
            
            self.service_status.set("🚀 Starting Flask service directly...")
            
            # Start Flask service as fallback
            self.flask_process = subprocess.Popen([
                sys.executable, app_path
            ], creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
            
            # Check if started successfully after a delay
            self.root.after(3000, self.verify_start)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start service:\n{e}")
            self.check_service_status()
            
    def verify_start(self):
        """Verify that service started successfully"""
        if not self.check_port_available(5000):
            messagebox.showinfo("Success", 
                              "✅ Disease Prediction Service started successfully!\n\n"
                              "You can now access it at:\nhttp://127.0.0.1:5000")
        else:
            messagebox.showwarning("Warning", 
                                 "Service may still be starting...\n"
                                 "Please wait a moment and refresh status.")
        
        self.check_service_status()
        
    def stop_service(self):
        """Stop the Flask service"""
        try:
            if self.flask_process:
                self.flask_process.terminate()
                self.flask_process = None
                
            messagebox.showinfo("Stopped", "Service stopped successfully!")
            self.check_service_status()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping service:\n{e}")
            
    def open_service(self):
        """Open the disease prediction service in browser"""
        import webbrowser
        webbrowser.open("http://127.0.0.1:5000")

def main():
    """Main function"""
    root = tk.Tk()
    app = KrishiVaaniServiceManager(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()