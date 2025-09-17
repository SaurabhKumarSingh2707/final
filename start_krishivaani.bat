@echo off
REM KrishiVaani Enhanced Auto-Start Batch Script
REM This script automatically starts Flask app when you access the main page

echo =========================================
echo   KrishiVaani Auto-Start System
echo =========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install required packages if needed
echo Checking Python packages...
pip install psutil flask tensorflow pillow numpy scikit-learn >nul 2>&1

echo Starting Enhanced KrishiVaani System...
echo.

REM Start the enhanced manager which includes HTTP bridge
python enhanced_krishivaani_manager.py

echo.
echo All services stopped.
echo Press any key to exit...
pause >nul