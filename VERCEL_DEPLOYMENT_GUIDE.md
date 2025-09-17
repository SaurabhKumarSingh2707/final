# Vercel Serverless Deployment Guide

## Overview
Your KrishiVaani project has been converted to work with Vercel serverless functions. This guide will help you deploy it successfully.

## 🚀 Quick Start

### 1. Prerequisites
- Vercel account (free at vercel.com)
- GitHub repository
- Model files (`best_model.h5`, `class_names.txt`, etc.)

### 2. Project Structure
```
Agri/
├── vercel.json                 # Vercel configuration
├── requirements.txt            # Python dependencies
├── disease_prediction_app.html # Main prediction interface
├── dashboard.html              # Updated dashboard
├── api/                        # Serverless functions
│   ├── _utils.py              # Shared utilities
│   ├── predict.py             # Single image prediction
│   ├── batch_predict.py       # Batch prediction
│   ├── model_info.py          # Model information
│   └── health.py              # Health check
├── crop-disease/               # Model files and prediction logic
│   ├── predict_advanced.py
│   ├── best_model.h5
│   ├── class_names.txt
│   └── ...
└── ... (other files)
```

## 📋 Deployment Steps

### Step 1: Prepare Your Repository
1. **Commit all changes** to your GitHub repository
2. **Ensure model files are included** (if they're large, see Model Handling section)
3. **Verify file structure** matches the above

### Step 2: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. **Root Directory**: Set to `Agri` (the folder containing vercel.json)
5. **Framework Preset**: Other
6. Click "Deploy"

### Step 3: Configure Environment (if needed)
In Vercel dashboard, go to Settings > Environment Variables:
```
PYTHONPATH=.
TF_CPP_MIN_LOG_LEVEL=2
```

## 🔧 Important Configuration Details

### Vercel.json Configuration
The `vercel.json` file is already configured with:
- Python 3.9 runtime
- Appropriate timeouts for ML processing
- CORS handling
- Route mappings

### API Endpoints
After deployment, your APIs will be available at:
- `https://your-domain.vercel.app/api/predict` - Single prediction
- `https://your-domain.vercel.app/api/batch_predict` - Batch prediction  
- `https://your-domain.vercel.app/api/model_info` - Model information
- `https://your-domain.vercel.app/api/health` - Health check

### Frontend Updates
Your JavaScript files have been updated to automatically detect:
- **Local development**: Uses `http://127.0.0.1:5000` (Flask)
- **Production**: Uses Vercel API endpoints

## 📦 Model Files Handling

### Small Models (< 100MB)
- Include directly in repository
- Files in `crop-disease/` directory will be deployed

### Large Models (> 100MB)
**Option 1: Git LFS**
```bash
git lfs track "*.h5"
git add .gitattributes
git add crop-disease/best_model.h5
git commit -m "Add model with LFS"
```

**Option 2: External Storage**
- Upload models to AWS S3, Google Cloud Storage, etc.
- Modify `_utils.py` to download models on cold start
- Use environment variables for storage URLs

**Option 3: Model Optimization**
- Use the provided `compress_model.py` to reduce size
- Convert to TensorFlow Lite if possible

## 🚨 Important Limitations

### Vercel Limitations
- **Function timeout**: 30-60 seconds max
- **Memory**: 1GB max for Pro plans
- **Package size**: 250MB max
- **Cold starts**: First request may be slow

### Workarounds
1. **Optimize model size** using compression
2. **Use caching** for frequently accessed models
3. **Implement warming functions** to reduce cold starts
4. **Consider alternatives** for very large models

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-domain.vercel.app/api/health
```

### 2. Model Info
```bash
curl https://your-domain.vercel.app/api/model_info
```

### 3. Prediction Test
Use the web interface at:
`https://your-domain.vercel.app/disease_prediction_app.html`

## 🔄 Local vs Production Behavior

### Local Development (localhost)
- Uses Flask server on port 5000
- Batch files (.bat) can execute
- Full file system access

### Production (Vercel)
- Uses serverless API functions
- No batch file execution
- Limited file system access
- Automatic scaling

## 🛠️ Troubleshooting

### Common Issues

**1. Model Loading Errors**
```
Error: Model file not found
```
- Check model files are in `crop-disease/` directory
- Verify file paths in `_utils.py`
- Check Vercel deployment logs

**2. Timeout Errors**
```
Error: Function timed out
```
- Reduce model size
- Optimize prediction code
- Increase timeout in `vercel.json`

**3. Package Size Errors**
```
Error: Package size exceeded
```
- Remove unnecessary dependencies from `requirements.txt`
- Compress model files
- Use `.vercelignore` to exclude files

**4. CORS Issues**
```
Error: CORS policy blocked
```
- Check CORS headers in API functions
- Verify domain configuration

### Debugging Steps
1. **Check Vercel logs**: Dashboard > Functions > View Logs
2. **Test APIs directly**: Use Postman or curl
3. **Verify file structure**: Ensure all files deployed correctly
4. **Check environment variables**: Verify configuration

## 📊 Performance Optimization

### Cold Start Reduction
1. **Keep models small** (< 50MB preferred)
2. **Minimize dependencies** in requirements.txt
3. **Use warming functions** for critical APIs
4. **Cache model loading** in global variables

### Request Optimization
1. **Compress images** before sending
2. **Use appropriate image sizes** (224x224 or 300x300)
3. **Implement client-side caching**
4. **Add request debouncing**

## 🎯 Next Steps After Deployment

1. **Test all functionality** thoroughly
2. **Monitor performance** in Vercel dashboard
3. **Set up domain** (optional)
4. **Configure analytics** (optional)
5. **Set up monitoring alerts**

## 🔧 Alternative Deployment Options

If Vercel doesn't work for your model size:

### Option A: Railway
- Better for larger applications
- Persistent storage
- Docker support

### Option B: Heroku
- Traditional web app deployment
- Supports larger files
- Persistent file system

### Option C: Google Cloud Run
- Serverless containers
- More memory/storage options
- Better for heavy ML workloads

## 📞 Support

If you encounter issues:
1. Check Vercel documentation
2. Review deployment logs
3. Test locally first
4. Consider model optimization
5. Use alternative hosting if needed

Your project is now ready for Vercel deployment! 🚀