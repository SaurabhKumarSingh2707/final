@echo off
title KrishiVaani Disease Prediction Service
echo.
echo ================================================================
echo               KrishiVaani Disease Prediction Service
echo ================================================================
echo.
echo Starting the Flask disease prediction service...
echo.

cd /d "%~dp0"
python simple_flask_launcher.py

echo.
echo ================================================================
echo Service launcher completed.
echo If the service is running, you can access it at:
echo http://127.0.0.1:5000
echo ================================================================
echo.
pause