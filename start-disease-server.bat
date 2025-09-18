@echo off
echo ================================
echo KrishiVaani Disease Prediction Server
echo ================================
echo.
echo Starting AI Disease Prediction Service...
echo.

cd /d "%~dp0crop-disease-clean-main"

if not exist "app_advanced.py" (
    echo Error: app_advanced.py not found in crop-disease-clean-main folder
    echo Please make sure you're running this from the correct directory
    pause
    exit /b 1
)

if not exist "best_model.h5" (
    echo Warning: best_model.h5 not found
    echo The model file might be missing or need to be downloaded
    echo.
)

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo.
echo Installing/Checking required packages...
pip install flask pillow numpy tensorflow >nul 2>&1

echo.
echo ================================
echo Starting Flask Server...
echo ================================
echo.
echo The server will start on http://127.0.0.1:5000
echo.
echo Keep this window open while using the disease prediction feature
echo Press Ctrl+C to stop the server
echo.

python app_advanced.py

echo.
echo Server stopped.
pause