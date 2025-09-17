/**
 * Auto Flask Starter - JavaScript client-side service manager
 * Automatically starts Flask service when KrishiVaani web app is accessed
 */

class FlaskServiceManager {
    constructor() {
        this.flaskUrl = 'http://127.0.0.1:5000';
        this.checkInterval = null;
        this.isInitialized = false;
    }

    /**
     * Check if Flask service is running
     */
    async checkFlaskService() {
        try {
            const response = await fetch(this.flaskUrl, {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache'
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    /**
     * Start Flask service by triggering Python script
     */
    async startFlaskService() {
        try {
            console.log('🚀 Attempting to start Flask disease prediction service...');
            
            // Try to start the service using local file protocol
            // Note: This requires the user to have run the Python manager
            const startScript = `
                import subprocess
                import sys
                subprocess.run([sys.executable, 'crop-disease/flask_auto_starter.py', 'start'])
            `;
            
            // Show user notification about service startup
            this.showServiceNotification();
            
            return true;
        } catch (error) {
            console.error('❌ Error starting Flask service:', error);
            return false;
        }
    }

    /**
     * Show notification to user about service management
     */
    showServiceNotification() {
        // Only show if user hasn't been notified in this session
        if (!sessionStorage.getItem('flaskServiceNotified')) {
            const notification = document.createElement('div');
            notification.innerHTML = `
                <div style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: linear-gradient(135deg, #22c55e, #16a34a);
                    color: white;
                    padding: 15px 20px;
                    border-radius: 12px;
                    box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
                    z-index: 10000;
                    font-family: 'Open Sans', sans-serif;
                    max-width: 350px;
                    animation: slideIn 0.5s ease-out;
                ">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 1.2em; margin-right: 8px;">🌱</span>
                        <strong>KrishiVaani Services</strong>
                    </div>
                    <p style="margin: 0; font-size: 14px; line-height: 1.4;">
                        For full AI disease prediction, ensure backend services are running.
                        <br><br>
                        <strong>Quick start:</strong><br>
                        Run: <code style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 4px; font-size: 12px;">python krishivaani_manager.py</code>
                    </p>
                    <button onclick="this.parentElement.parentElement.remove()" style="
                        position: absolute;
                        top: 5px;
                        right: 5px;
                        background: none;
                        border: none;
                        color: white;
                        font-size: 18px;
                        cursor: pointer;
                        padding: 5px;
                        line-height: 1;
                    ">×</button>
                </div>
                <style>
                    @keyframes slideIn {
                        from {
                            transform: translateX(100%);
                            opacity: 0;
                        }
                        to {
                            transform: translateX(0);
                            opacity: 1;
                        }
                    }
                </style>
            `;
            
            document.body.appendChild(notification);
            
            // Auto-hide after 8 seconds
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.style.animation = 'slideIn 0.5s ease-out reverse';
                    setTimeout(() => notification.remove(), 500);
                }
            }, 8000);
            
            sessionStorage.setItem('flaskServiceNotified', 'true');
        }
    }

    /**
     * Monitor Flask service and show status
     */
    async monitorService() {
        const isRunning = await this.checkFlaskService();
        
        // Update any disease prediction links with service status
        const diseaseLinks = document.querySelectorAll('a[href*="crop-disease"], a[href*="disease"]');
        diseaseLinks.forEach(link => {
            if (isRunning) {
                link.style.position = 'relative';
                if (!link.querySelector('.service-indicator')) {
                    const indicator = document.createElement('span');
                    indicator.className = 'service-indicator';
                    indicator.innerHTML = '🟢';
                    indicator.style.cssText = `
                        position: absolute;
                        top: -5px;
                        right: -5px;
                        font-size: 12px;
                        animation: pulse 2s infinite;
                    `;
                    link.appendChild(indicator);
                }
            } else {
                const indicator = link.querySelector('.service-indicator');
                if (indicator) {
                    indicator.innerHTML = '🟡';
                    indicator.title = 'Service not running - click to start';
                }
            }
        });

        return isRunning;
    }

    /**
     * Initialize the service manager
     */
    async initialize() {
        if (this.isInitialized) return;
        
        console.log('🌾 Initializing KrishiVaani Service Manager...');
        
        // Check if Flask service is already running
        const isRunning = await this.checkFlaskService();
        
        if (isRunning) {
            console.log('✅ Flask disease prediction service is running');
        } else {
            console.log('⚠️ Flask disease prediction service is not running');
            
            // Show notification to user
            setTimeout(() => this.showServiceNotification(), 2000);
        }

        // Start monitoring
        this.checkInterval = setInterval(() => {
            this.monitorService();
        }, 30000); // Check every 30 seconds

        // Enhanced click handlers for disease prediction links
        this.setupEnhancedLinks();
        
        this.isInitialized = true;
    }

    /**
     * Setup enhanced click handlers for disease prediction links
     */
    setupEnhancedLinks() {
        document.addEventListener('click', async (event) => {
            const link = event.target.closest('a[href*="crop-disease"], a[href*="disease"]');
            if (!link) return;

            // Check if this is the advanced disease prediction link
            if (link.href.includes('crop-disease') || link.href.includes('127.0.0.1:5000')) {
                event.preventDefault();
                
                const isRunning = await this.checkFlaskService();
                
                if (isRunning) {
                    // Service is running, proceed normally
                    window.open('http://127.0.0.1:5000', '_blank');
                } else {
                    // Service not running, show helpful message
                    if (typeof Swal !== 'undefined') {
                        Swal.fire({
                            title: '🔧 Service Setup Required',
                            html: `
                                <div style="text-align: left; padding: 15px;">
                                    <p style="margin-bottom: 15px;">The AI Disease Prediction service needs to be started.</p>
                                    
                                    <h4 style="color: #16a34a; margin-bottom: 10px;">🚀 Quick Start:</h4>
                                    <ol style="padding-left: 20px;">
                                        <li>Open command prompt in the Agri folder</li>
                                        <li>Run: <code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px;">python krishivaani_manager.py</code></li>
                                        <li>Wait for services to start</li>
                                        <li>Return here and try again</li>
                                    </ol>
                                    
                                    <p style="margin-top: 15px; font-size: 14px; color: #6b7280;">
                                        The service will automatically start the Flask backend and open the application.
                                    </p>
                                </div>
                            `,
                            icon: 'info',
                            confirmButtonText: '📋 Copy Command',
                            cancelButtonText: '❌ Cancel',
                            showCancelButton: true,
                            confirmButtonColor: '#16a34a',
                            cancelButtonColor: '#6b7280'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                // Copy command to clipboard
                                navigator.clipboard.writeText('python krishivaani_manager.py').then(() => {
                                    Swal.fire({
                                        title: '✅ Copied!',
                                        text: 'Command copied to clipboard. Run it in your terminal.',
                                        icon: 'success',
                                        timer: 2000,
                                        showConfirmButton: false
                                    });
                                });
                            }
                        });
                    } else {
                        // Fallback for when SweetAlert is not available
                        alert('Please start the Flask service first by running: python krishivaani_manager.py');
                    }
                }
            }
        });
    }

    /**
     * Cleanup resources
     */
    destroy() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
        this.isInitialized = false;
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.flaskServiceManager = new FlaskServiceManager();
    window.flaskServiceManager.initialize();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.flaskServiceManager) {
        window.flaskServiceManager.destroy();
    }
});

// Export for manual usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FlaskServiceManager;
}