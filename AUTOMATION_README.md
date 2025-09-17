# KrishiVaani README - Automated Startup Guide

## 🚀 Quick Start Options

### Option 1: One-Click Windows Start
```bash
# Double-click this file:
start_krishivaani.bat
```

### Option 2: Python Manager
```bash
# From the Agri directory:
python krishivaani_manager.py

# Or with specific commands:
python krishivaani_manager.py start    # Start all services
python krishivaani_manager.py stop     # Stop all services  
python krishivaani_manager.py status   # Check status
```

### Option 3: Direct Flask Control
```bash
# From the crop-disease directory:
python flask_auto_starter.py start     # Start Flask service
python flask_auto_starter.py stop      # Stop Flask service
python flask_auto_starter.py status    # Check Flask status
python flask_auto_starter.py daemon    # Run as background daemon
```

## 🔧 How Automation Works

### Web Integration
- The `flask-service-manager.js` script automatically detects when Flask services are needed
- Shows helpful notifications and status indicators
- Provides one-click service management from the web interface

### Backend Management
- `krishivaani_manager.py` handles the complete startup sequence
- `flask_auto_starter.py` manages the Flask disease prediction service
- Automatic service monitoring and restart capabilities

### Smart Features
- ✅ Service health monitoring
- 🔄 Automatic restarts on failure
- 📊 Real-time status indicators in web UI
- 🚨 User-friendly error messages and guidance
- 💾 Process management and cleanup

## 📁 Service Files Created

```
Agri/
├── krishivaani_manager.py          # Main service manager
├── flask-service-manager.js        # Web-based service control
├── start_krishivaani.bat          # Windows one-click starter
└── crop-disease/
    ├── flask_auto_starter.py       # Flask service manager
    ├── app_advanced.py             # Main Flask application
    └── predict_advanced.py         # AI prediction engine
```

## 🌟 User Experience

1. **Automatic Detection**: Web app detects when backend services are needed
2. **Smart Notifications**: Helpful guidance when services aren't running
3. **One-Click Start**: Multiple easy ways to start services
4. **Visual Indicators**: Status indicators show service health
5. **Error Handling**: Graceful handling of service issues

## 💡 Tips

- Services automatically restart if they crash
- Web interface provides real-time service status
- Use the batch file for quickest startup on Windows
- Daemon mode keeps services running in background
- All logs are saved for troubleshooting