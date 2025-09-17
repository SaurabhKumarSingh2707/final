#!/usr/bin/env bash
# Render deployment script

echo "🚀 Starting deployment..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔍 Checking model files..."

# Check if compressed model exists and decompress it
if [ -f "model_phase1.h5.gz" ]; then
    echo "📦 Found compressed model, decompressing..."
    python compress_model.py auto
else
    echo "⚠️ No compressed model found, checking for existing model..."
    if [ -f "model_phase1.h5" ]; then
        echo "✅ Found existing model file"
    elif [ -f "best_model.h5" ]; then
        echo "✅ Found best_model.h5"
    else
        echo "❌ No model files found!"
        exit 1
    fi
fi

echo "📁 Creating uploads directory..."
mkdir -p uploads

echo "🔧 Setting permissions..."
chmod -R 755 uploads

echo "✅ Deployment script completed successfully"