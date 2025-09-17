/**
 * Advanced Flask Auto-Starter for KrishiVaani
 * Automatically detects and starts Flask app when main page is accessed
 */

class AdvancedFlaskAutoStarter {
    constructor() {
        this.flaskUrl = 'http://127.0.0.1:5000';
        this.serviceCheckInterval = null;
        this.startupAttempts = 0;
        this.maxStartupAttempts = 3;
        this.isStarting = false;
        this.serviceStatus = 'unknown';
        
        // Bind methods
        this.checkService = this.checkService.bind(this);
        this.startFlaskService = this.startFlaskService.bind(this);
        this.handleServiceStart = this.handleServiceStart.bind(this);
    }

    /**
     * Check if Flask service is running
     */
    async checkService() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout
            
            const response = await fetch(this.flaskUrl, {
                method: 'HEAD',
                mode: 'cors',
                cache: 'no-cache',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                this.serviceStatus = 'running';
                this.updateServiceIndicators(true);
                return true;
            } else {
                this.serviceStatus = 'error';
                this.updateServiceIndicators(false);
                return false;
            }
        } catch (error) {
            this.serviceStatus = 'stopped';
            this.updateServiceIndicators(false);
            return false;
        }
    }

    /**
     * Start Flask service using Python subprocess approach
     */
    async startFlaskService() {
        if (this.isStarting) {
            console.log('Flask service startup already in progress...');
            return false;
        }

        this.isStarting = true;
        this.startupAttempts++;

        try {
            console.log('🚀 Attempting to start Flask disease prediction service...');
            
            // Show loading indicator
            this.showServiceStartupIndicator();
            
            // Try to trigger the Python manager
            const success = await this.triggerPythonServiceStart();
            
            if (success) {
                // Wait for service to be available (up to 30 seconds)
                const serviceReady = await this.waitForService(30000);
                
                if (serviceReady) {
                    console.log('✅ Flask service started successfully!');
                    this.showSuccessNotification();
                    this.serviceStatus = 'running';
                    return true;
                } else {
                    console.log('⚠️ Service started but not responding yet');
                    this.showServiceStartupGuidance();
                    return false;
                }
            } else {
                console.log('❌ Failed to start Flask service');
                this.showServiceStartupGuidance();
                return false;
            }
        } catch (error) {
            console.error('Error starting Flask service:', error);
            this.showServiceStartupGuidance();
            return false;
        } finally {
            this.isStarting = false;
            this.hideServiceStartupIndicator();
        }
    }

    /**
     * Trigger Python service start using various methods
     */
    async triggerPythonServiceStart() {
        // Method 1: Try to use the browser-triggered Flask manager
        try {
            console.log('🔗 Attempting to start Flask service via HTTP manager...');
            
            const response = await fetch('http://127.0.0.1:8765/start', {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    console.log('✅ Flask service started via HTTP manager');
                    return true;
                } else {
                    console.log('⚠️ HTTP manager responded but service failed to start');
                }
            } else {
                console.log('⚠️ HTTP manager not available');
            }
        } catch (error) {
            console.log('ℹ️ HTTP manager method failed (expected if not running):', error.message);
        }

        // Method 2: Try to use service worker if available
        if ('serviceWorker' in navigator) {
            try {
                console.log('🔄 Attempting service worker method...');
                await navigator.serviceWorker.register('/flask-service-worker.js');
                const registration = await navigator.serviceWorker.ready;
                
                if (registration.active) {
                    registration.active.postMessage({
                        command: 'start-flask',
                        data: { service: 'disease-prediction' }
                    });
                    console.log('📨 Service worker notified');
                    return true;
                }
            } catch (e) {
                console.log('ℹ️ Service worker method failed:', e.message);
            }
        }

        // Method 3: Try direct automation commands
        try {
            console.log('🎯 Attempting direct automation...');
            
            // Try to trigger existing automation system
            if (window.krishivaaniManager) {
                const result = await window.krishivaaniManager.start_flask_service();
                if (result) {
                    console.log('✅ Direct automation successful');
                    return true;
                }
            }
            
            // Try to trigger existing Flask service manager
            if (window.flaskServiceManager) {
                const result = await window.flaskServiceManager.startFlaskService();
                if (result) {
                    console.log('✅ Flask service manager successful');
                    return true;
                }
            }
        } catch (error) {
            console.log('ℹ️ Direct automation failed:', error.message);
        }

        // Method 4: Show user guidance for manual start
        console.log('📖 All automatic methods failed, showing user guidance');
        setTimeout(() => this.showServiceStartupGuidance(), 1000);
        return false;
    }

    /**
     * Wait for service to become available
     */
    async waitForService(timeout = 30000) {
        const startTime = Date.now();
        const checkInterval = 2000; // Check every 2 seconds

        while (Date.now() - startTime < timeout) {
            const isRunning = await this.checkService();
            if (isRunning) {
                return true;
            }
            await new Promise(resolve => setTimeout(resolve, checkInterval));
        }
        return false;
    }

    /**
     * Update service indicators in the UI
     */
    updateServiceIndicators(isRunning) {
        // Update disease prediction links
        const diseaseLinks = document.querySelectorAll('a[href*="crop-disease"], a[href*="disease"], [data-service="disease-prediction"]');
        
        diseaseLinks.forEach(link => {
            // Remove existing indicators
            const existingIndicator = link.querySelector('.service-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }

            // Add new indicator
            const indicator = document.createElement('span');
            indicator.className = 'service-indicator';
            indicator.style.cssText = `
                position: absolute;
                top: -5px;
                right: -5px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                font-size: 10px;
                line-height: 12px;
                text-align: center;
                z-index: 1000;
                animation: pulse 2s infinite;
            `;

            if (isRunning) {
                indicator.style.background = '#22c55e';
                indicator.innerHTML = '●';
                indicator.title = 'AI Service Running';
                link.style.position = 'relative';
            } else {
                indicator.style.background = '#f59e0b';
                indicator.innerHTML = '●';
                indicator.title = 'AI Service Stopped - Click to start';
                link.style.position = 'relative';
            }

            link.appendChild(indicator);
        });

        // Update any status displays
        const statusElements = document.querySelectorAll('.flask-service-status');
        statusElements.forEach(element => {
            element.textContent = isRunning ? 'AI Service: Online' : 'AI Service: Offline';
            element.className = `flask-service-status ${isRunning ? 'online' : 'offline'}`;
        });
    }

    /**
     * Show service startup indicator
     */
    showServiceStartupIndicator() {
        // Remove existing indicator
        const existing = document.getElementById('flask-startup-indicator');
        if (existing) existing.remove();

        const indicator = document.createElement('div');
        indicator.id = 'flask-startup-indicator';
        indicator.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
                z-index: 10001;
                font-family: 'Open Sans', sans-serif;
                font-size: 14px;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 10px;
                animation: slideDown 0.5s ease-out;
            ">
                <div style="
                    width: 16px;
                    height: 16px;
                    border: 2px solid transparent;
                    border-top: 2px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                "></div>
                Starting AI Disease Prediction Service...
            </div>
            <style>
                @keyframes slideDown {
                    from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
                    to { transform: translateX(-50%) translateY(0); opacity: 1; }
                }
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            </style>
        `;
        
        document.body.appendChild(indicator);
    }

    /**
     * Hide service startup indicator
     */
    hideServiceStartupIndicator() {
        const indicator = document.getElementById('flask-startup-indicator');
        if (indicator) {
            indicator.style.animation = 'slideDown 0.5s ease-out reverse';
            setTimeout(() => indicator.remove(), 500);
        }
    }

    /**
     * Show success notification
     */
    showSuccessNotification() {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                title: '🚀 AI Service Ready!',
                html: `
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 3rem; margin-bottom: 15px;">🤖</div>
                        <p style="font-size: 16px; color: #6b7280; margin-bottom: 20px;">
                            Advanced Plant Disease Prediction is now online and ready to use!
                        </p>
                        <div style="background: linear-gradient(135deg, #dcfce7, #bbf7d0); padding: 15px; border-radius: 12px; margin-bottom: 15px;">
                            <p style="color: #166534; font-weight: 600; margin: 0;">
                                🌐 Service URL: <code>http://127.0.0.1:5000</code>
                            </p>
                        </div>
                    </div>
                `,
                icon: null,
                confirmButtonText: '🌱 Open Disease Prediction',
                cancelButtonText: '👍 Continue',
                showCancelButton: true,
                confirmButtonColor: '#22c55e',
                cancelButtonColor: '#6b7280',
                timer: 5000,
                timerProgressBar: true
            }).then((result) => {
                if (result.isConfirmed) {
                    window.open('http://127.0.0.1:5000', '_blank');
                }
            });
        } else {
            // Fallback notification
            this.showSimpleNotification('AI Service Started Successfully!', 'success');
        }
    }

    /**
     * Show service startup guidance
     */
    showServiceStartupGuidance() {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                title: '🔧 Manual Service Start Required',
                html: `
                    <div style="text-align: left; padding: 15px;">
                        <p style="margin-bottom: 20px; color: #6b7280;">
                            The AI Disease Prediction service needs to be started manually.
                        </p>
                        
                        <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                            <h4 style="color: #1f2937; margin: 0 0 10px 0; font-size: 16px;">🚀 Quick Start Options:</h4>
                            
                            <div style="margin-bottom: 15px;">
                                <strong>Option 1 - One Click (Windows):</strong><br>
                                <code style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px;">Double-click: start_krishivaani.bat</code>
                            </div>
                            
                            <div style="margin-bottom: 15px;">
                                <strong>Option 2 - Command Line:</strong><br>
                                <code style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px;">python krishivaani_manager.py</code>
                            </div>
                            
                            <div>
                                <strong>Option 3 - Direct Flask:</strong><br>
                                <code style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px;">python crop-disease/flask_auto_starter.py start</code>
                            </div>
                        </div>
                        
                        <p style="font-size: 14px; color: #6b7280; margin: 0;">
                            After starting, the service will be available at <strong>http://127.0.0.1:5000</strong>
                        </p>
                    </div>
                `,
                icon: 'info',
                confirmButtonText: '📋 Copy Command',
                cancelButtonText: '✅ Got it',
                showCancelButton: true,
                confirmButtonColor: '#3b82f6',
                cancelButtonColor: '#6b7280',
                width: '600px'
            }).then((result) => {
                if (result.isConfirmed) {
                    navigator.clipboard.writeText('python krishivaani_manager.py').then(() => {
                        Swal.fire({
                            title: '📋 Copied!',
                            text: 'Command copied to clipboard. Run it in your terminal.',
                            icon: 'success',
                            timer: 2000,
                            showConfirmButton: false
                        });
                    });
                }
            });
        } else {
            alert('Please start the Flask service by running: python krishivaani_manager.py');
        }
    }

    /**
     * Show simple notification fallback
     */
    showSimpleNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            font-family: 'Open Sans', sans-serif;
            animation: slideIn 0.5s ease-out;
            max-width: 300px;
        `;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span>${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: none; border: none; color: white; 
                    font-size: 18px; cursor: pointer; margin-left: auto;
                ">×</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }

    /**
     * Setup enhanced link handlers
     */
    setupEnhancedLinkHandlers() {
        document.addEventListener('click', async (event) => {
            const link = event.target.closest('a[href*="crop-disease"], a[href*="127.0.0.1:5000"], [data-service="disease-prediction"]');
            if (!link) return;

            // Check if this is a disease prediction link
            const isDiseaseLink = link.href.includes('crop-disease') || 
                                 link.href.includes('127.0.0.1:5000') || 
                                 link.dataset.service === 'disease-prediction';

            if (isDiseaseLink) {
                event.preventDefault();
                
                const isRunning = await this.checkService();
                
                if (isRunning) {
                    // Service is running, open it
                    window.open('http://127.0.0.1:5000', '_blank');
                } else {
                    // Service not running, try to start it
                    if (this.startupAttempts < this.maxStartupAttempts) {
                        const started = await this.startFlaskService();
                        if (started) {
                            // Service started, open it
                            setTimeout(() => {
                                window.open('http://127.0.0.1:5000', '_blank');
                            }, 2000);
                        }
                    } else {
                        // Max attempts reached, show guidance
                        this.showServiceStartupGuidance();
                    }
                }
            }
        });
    }

    /**
     * Initialize the auto-starter
     */
    async initialize() {
        console.log('🌾 Initializing Advanced Flask Auto-Starter...');
        
        // Check initial service status
        const isRunning = await this.checkService();
        
        if (isRunning) {
            console.log('✅ Flask service is already running');
            this.serviceStatus = 'running';
        } else {
            console.log('⚠️ Flask service is not running');
            this.serviceStatus = 'stopped';
            
            // Auto-attempt to start service on page load
            setTimeout(() => {
                if (this.startupAttempts === 0) {
                    this.startFlaskService();
                }
            }, 2000);
        }

        // Setup link handlers
        this.setupEnhancedLinkHandlers();

        // Start monitoring service status
        this.serviceCheckInterval = setInterval(this.checkService, 30000); // Check every 30 seconds

        console.log('🚀 Advanced Flask Auto-Starter initialized');
    }

    /**
     * Cleanup resources
     */
    destroy() {
        if (this.serviceCheckInterval) {
            clearInterval(this.serviceCheckInterval);
            this.serviceCheckInterval = null;
        }
        
        // Remove any indicators
        document.querySelectorAll('.service-indicator').forEach(el => el.remove());
        const startupIndicator = document.getElementById('flask-startup-indicator');
        if (startupIndicator) startupIndicator.remove();
        
        console.log('🧹 Advanced Flask Auto-Starter cleaned up');
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait a moment for other scripts to load
    setTimeout(() => {
        window.advancedFlaskAutoStarter = new AdvancedFlaskAutoStarter();
        window.advancedFlaskAutoStarter.initialize();
    }, 1000);
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.advancedFlaskAutoStarter) {
        window.advancedFlaskAutoStarter.destroy();
    }
});

// Export for manual usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedFlaskAutoStarter;
}

// Global helper function for manual service management
window.startFlaskService = function() {
    if (window.advancedFlaskAutoStarter) {
        return window.advancedFlaskAutoStarter.startFlaskService();
    }
    return false;
};