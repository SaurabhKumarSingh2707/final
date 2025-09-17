#  Getting Started with AgriTech Frontend

Welcome to the AgriTech Frontend project! This is a pure HTML/CSS/JavaScript agricultural platform.

##  Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- No server setup required!

##  Quick Start

1. **Download/Clone the Project**
   ```bash
   # If you have git installed
   git clone [repository-url]
   
   # Or simply download and extract the ZIP file
   ```

2. **Open in Browser**
   - Navigate to the project folder
   - Double-click `index.html` OR
   - Right-click `index.html`  Open with  Your Browser

3. **Explore the Platform**
   - Start with the homepage (`index.html`)
   - Navigate to the dashboard (`dashboard.html`)
   - Try different agricultural tools and guides

##  Key Features

###  Homepage (`index.html`)
- Clean landing page with feature overview
- Theme toggle (Dark/Light mode)
- Navigation to all sections

###  Dashboard (`dashboard.html`)
- Main hub for all agricultural tools
- Interactive cards for each feature
- Smart loan calculator integration

###  Agricultural Tools
- **Crop Recommendation** (`crop-recommendation.html`)
- **Yield Prediction** (`crop-yield.html`)
- **Crop Planning** (`crop-planning.html`)
- **Labour Alerts** (`labour-alerts.html`)

###  Information Pages
- **Weather Tracking** (`weather.html`)
- **Disease Guide** (`disease.html`)
- **Farmer Network** (`farmer.html`)
- **Organic Farming** (`organic.html`)
- **Plantation Guide** (`plantation.html`)

##  Customization

### Changing Colors
Edit `style.css` and look for CSS custom properties:
```css
:root {
  --primary-color: #2e7d32;
  --secondary-color: #4caf50;
}
```

### Adding New Pages
1. Create new HTML file following existing structure
2. Include standard CSS and JS files
3. Add navigation links in relevant pages

### Modifying Content
- Edit HTML files directly for content changes
- Update JavaScript for functionality changes
- Modify CSS for styling changes

##  File Structure

```
AgriTech-Frontend/
 index.html                 # Homepage
 dashboard.html             # Main dashboard
 crop-recommendation.html   # Crop recommendation tool
 crop-yield.html           # Yield prediction tool
 crop-planning.html        # Crop planning calendar
 labour-alerts.html        # Alerts and notifications
 [other-pages].html        # Additional pages
 style.css                 # Main stylesheet
 main.css                  # Dashboard styles
 theme.css                 # Theme management
 [other].css               # Page-specific styles
 [various].js              # JavaScript functionality
 images/                   # Static images
```

##  Development Tips

### Local Development
- Use VS Code Live Server extension for better development experience
- Open browser developer tools to debug JavaScript
- Use browser's responsive mode to test mobile view

### Adding Interactivity
- Check existing JavaScript patterns in current files
- Use `localStorage` for data persistence
- Follow existing naming conventions

### Responsive Design
- Most pages are mobile-friendly
- Test on different screen sizes
- Modify CSS media queries as needed

##  Browser Support

-  Chrome (recommended)
-  Firefox
-  Safari
-  Edge
-  Mobile browsers

##  Usage Examples

### Theme Switching
The platform supports dark/light themes:
```javascript
// Theme is automatically saved to localStorage
// Toggle button available in navigation
```

### Form Validation
Interactive forms with client-side validation:
```javascript
// Check crop-recommendation.html for form handling examples
```

### Local Storage
User preferences are saved:
```javascript
localStorage.setItem('theme', 'dark');
localStorage.getItem('theme');
```

##  Troubleshooting

### Images Not Loading
- Ensure `images/` folder is in the same directory
- Check image file names and extensions
- Verify image paths in HTML files

### JavaScript Not Working
- Check browser console for errors (F12)
- Ensure all JS files are in correct location
- Verify file paths in HTML

### Styling Issues
- Clear browser cache (Ctrl+F5)
- Check CSS file paths
- Verify CSS syntax

##  License

This project is open source and available under the MIT License.

##  Contributing

1. Fork the project
2. Make your changes
3. Test thoroughly
4. Submit a pull request

##  Support

- Check browser console for errors
- Ensure all files are in correct directories
- Test in different browsers
- Review existing code for patterns

---

**Happy Farming with AgriTech Frontend! **
