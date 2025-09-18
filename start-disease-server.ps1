# KrishiVaani Disease Prediction Server Startup Script
Write-Host "================================" -ForegroundColor Green
Write-Host "KrishiVaani Disease Prediction Server" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting AI Disease Prediction Service..." -ForegroundColor Yellow
Write-Host ""

# Change to the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$appPath = Join-Path $scriptPath "crop-disease-clean-main"

Set-Location $appPath

if (!(Test-Path "app_advanced.py")) {
    Write-Host "Error: app_advanced.py not found in crop-disease-clean-main folder" -ForegroundColor Red
    Write-Host "Please make sure you're running this from the correct directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (!(Test-Path "best_model.h5")) {
    Write-Host "Warning: best_model.h5 not found" -ForegroundColor Yellow
    Write-Host "The model file might be missing or need to be downloaded" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing/Checking required packages..." -ForegroundColor Cyan
pip install flask pillow numpy tensorflow | Out-Null

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Starting Flask Server..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "The server will start on http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Keep this window open while using the disease prediction feature" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    python app_advanced.py
} catch {
    Write-Host "Error starting the server" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"