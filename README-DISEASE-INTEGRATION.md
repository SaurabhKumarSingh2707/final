# KrishiVaani Disease Prediction Integration

This integration adds AI-powered plant disease prediction directly to the KrishiVaani dashboard.

## Features

✅ **Advanced AI Disease Detection**: Uses deep learning models for accurate plant disease identification  
✅ **Seamless Dashboard Integration**: Accessible directly from the main dashboard  
✅ **Real-time Predictions**: Instant analysis with confidence scores  
✅ **Treatment Recommendations**: Get actionable advice for disease treatment and prevention  
✅ **Multiple Image Formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF, WebP  
✅ **Test-Time Augmentation**: Advanced technique for improved accuracy  

## Quick Setup

### Option 1: Using Startup Scripts (Recommended)

1. **Double-click** `start-disease-server.bat` (Windows Batch) or run `start-disease-server.ps1` (PowerShell)
2. Wait for the message: `Running on http://127.0.0.1:5000`
3. Go to the dashboard and click **"Disease Prediction"**

### Option 2: Manual Setup

1. **Open Terminal/Command Prompt**
2. **Navigate to the disease prediction folder:**
   ```bash
   cd crop-disease-clean-main
   ```

3. **Install required packages:**
   ```bash
   pip install flask pillow numpy tensorflow
   ```

4. **Start the Flask server:**
   ```bash
   python app_advanced.py
   ```

5. **Wait for confirmation message:**
   ```
   🚀 Starting KrishiVannai AI Plant Disease Prediction App...
   🌐 Starting server on port 5000
   * Running on http://127.0.0.1:5000
   ```

## How to Use

1. **Start the server** (using steps above)
2. **Open dashboard** (`dashboard.html`)
3. **Click "Disease Prediction"** (either in navigation or card)
4. **Upload a plant image**
5. **Get instant AI analysis** with treatment recommendations

## Dashboard Integration Details

The integration includes:

- **Smart Server Detection**: Automatically checks if the Flask server is running
- **User-Friendly Setup**: Clear instructions when server isn't available
- **Seamless Navigation**: Direct access from dashboard navigation and cards
- **Professional UI**: Matches the dashboard's modern design
- **Error Handling**: Graceful handling of connection issues

## Files Added/Modified

### New Files:
- `disease-prediction-integrated.html` - Integrated disease prediction interface
- `start-disease-server.bat` - Windows batch startup script
- `start-disease-server.ps1` - PowerShell startup script
- `README-DISEASE-INTEGRATION.md` - This documentation

### Modified Files:
- `dashboard.html` - Updated navigation and added integration JavaScript

## Troubleshooting

### Server Won't Start
- Make sure Python is installed and in PATH
- Install required packages: `pip install flask pillow numpy tensorflow`
- Check if port 5000 is already in use

### "Service Unavailable" Error
- Ensure the Flask server is running on `http://127.0.0.1:5000`
- Check firewall/antivirus isn't blocking the connection
- Try restarting the server

### Model Not Found
- Ensure `best_model.h5` exists in the `crop-disease-clean-main` folder
- Check `class_names.txt` is also present
- Download missing model files if needed

### Network/CORS Issues
- Make sure both dashboard and Flask server are running on localhost
- Check browser console for detailed error messages
- Try refreshing the page after starting the server

## Technical Details

- **Backend**: Flask with TensorFlow/Keras for AI inference
- **Frontend**: Vanilla JavaScript with SweetAlert2 for notifications
- **Communication**: REST API with JSON responses
- **Model**: Deep learning CNN for plant disease classification
- **Features**: Test-Time Augmentation, confidence scoring, detailed analysis

## Dependencies

- Python 3.7+
- Flask
- TensorFlow/Keras
- Pillow (PIL)
- NumPy
- Modern web browser with JavaScript enabled

## Support

If you encounter issues:

1. Check the terminal/console for error messages
2. Ensure all dependencies are installed
3. Verify the model files are present
4. Make sure port 5000 is available

---

**Note**: Keep the terminal/command prompt window open while using the disease prediction feature. The Flask server must be running for the integration to work properly.