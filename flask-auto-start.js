/**
 * Simple Flask Auto-Start Integration
 * Automatically detects and manages Flask service when main page loads
 */

(function() {
    'use strict';
    
    // Configuration - Updated for Vercel deployment
    const CONFIG = {
        // Use current domain for production, localhost for development
        apiBaseUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? 'http://127.0.0.1:5000' 
            : window.location.origin,
        flaskUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? 'http://127.0.0.1:5000' 
            : `${window.location.origin}/api/health`,
        httpManagerUrl: 'http://127.0.0.1:8765', // Only for local development
        checkInterval: 30000, // 30 seconds
        startupDelay: 2000,   // 2 seconds
        maxRetries: 3,
        isProduction: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
    };
    
    let serviceChecker = null;
    let startupAttempts = 0;
    let isStarting = false;

    /**
     * Check if Flask service is running
     */
    async function checkFlaskService() {
        try {
            if (CONFIG.isProduction) {
                // In production, check the health endpoint
                const response = await fetch(`${CONFIG.apiBaseUrl}/api/health`, {
                    method: 'GET',
                    mode: 'cors',
                    cache: 'no-cache'
                });
                return response.ok;
            } else {
                // In development, check localhost Flask
                const response = await fetch(CONFIG.flaskUrl, {
                    method: 'HEAD',
                    mode: 'cors',
                    cache: 'no-cache'
                });
                return response.ok;
            }
        } catch (error) {
            return false;
        }
    }

    /**
     * Try to start Flask service via Start_Disease_Prediction.bat
     */
    async function startFlaskViaBatch() {
        try {
            // Only try batch execution in development mode
            if (CONFIG.isProduction) {
                console.log('🌱 In production mode - services should be auto-available');
                // In production, the serverless functions should already be available
                const running = await checkFlaskService();
                return running;
            }
            
            console.log('🌱 Attempting to run Start_Disease_Prediction.bat');
            
            // Method 1: Try to create and trigger a download of the batch file
            const link = document.createElement('a');
            link.href = 'Start_Disease_Prediction.bat';
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Method 2: Try using hidden iframe
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = 'Start_Disease_Prediction.bat';
            document.body.appendChild(iframe);
            
            setTimeout(() => {
                try {
                    document.body.removeChild(iframe);
                } catch (e) {
                    console.log('Iframe cleanup error:', e);
                }
            }, 2000);
            
            // Wait a moment for the batch file to potentially execute
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            // Check if service is now running
            const running = await checkFlaskService();
            if (running) {
                console.log('✅ Start_Disease_Prediction.bat execution successful');
                return true;
            }
            
            console.log('⚠️ Start_Disease_Prediction.bat may not have executed');
            return false;
            
        } catch (error) {
            console.log('Batch file execution failed:', error.message);
            return false;
        }
    }

    /**
     * Try to start Flask service via HTTP manager
     */
    async function startFlaskViaManager() {
        try {
            const response = await fetch(`${CONFIG.httpManagerUrl}/start`, {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache'
            });
            
            if (response.ok) {
                const result = await response.json();
                return result.success || false;
            }
            return false;
        } catch (error) {
            console.log('HTTP manager not available:', error.message);
            return false;
        }
    }

    /**
     * Show status notification
     */
    function showStatusNotification(message, type = 'info', duration = 4000) {
        // Remove existing notifications
        const existing = document.querySelector('.flask-auto-notification');
        if (existing) existing.remove();

        const notification = document.createElement('div');
        notification.className = 'flask-auto-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            font-family: 'Open Sans', sans-serif;
            font-size: 14px;
            font-weight: 500;
            max-width: 300px;
            animation: slideInRight 0.3s ease-out;
        `;

        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <span>${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: none; border: none; color: white; 
                    font-size: 16px; cursor: pointer; margin-left: auto; padding: 0;
                ">×</button>
            </div>
        `;

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        if (!document.querySelector('#flask-auto-styles')) {
            style.id = 'flask-auto-styles';
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);
        
        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.style.animation = 'slideInRight 0.3s ease-out reverse';
                    setTimeout(() => notification.remove(), 300);
                }
            }, duration);
        }
    }

    /**
     * Update UI indicators
     */
    function updateServiceIndicators(isRunning) {
        // Find all disease prediction related links
        const diseaseLinks = document.querySelectorAll(`
            a[href*="crop-disease"], 
            a[href*="disease"], 
            a[href*="127.0.0.1:5000"],
            [data-service="disease-prediction"]
        `);

        diseaseLinks.forEach(link => {
            // Remove existing indicators
            const existing = link.querySelector('.service-status-indicator');
            if (existing) existing.remove();

            // Add status indicator
            const indicator = document.createElement('span');
            indicator.className = 'service-status-indicator';
            indicator.style.cssText = `
                position: absolute;
                top: -3px;
                right: -3px;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: ${isRunning ? '#10b981' : '#f59e0b'};
                border: 2px solid white;
                z-index: 100;
                animation: pulse 2s infinite;
            `;
            indicator.title = isRunning ? 'AI Service Online' : 'AI Service Starting...';

            // Ensure parent is positioned
            if (getComputedStyle(link).position === 'static') {
                link.style.position = 'relative';
            }

            link.appendChild(indicator);
        });

        // Add pulse animation
        const pulseStyle = document.createElement('style');
        pulseStyle.textContent = `
            @keyframes pulse {
                0% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.7; transform: scale(1.1); }
                100% { opacity: 1; transform: scale(1); }
            }
        `;
        if (!document.querySelector('#pulse-animation')) {
            pulseStyle.id = 'pulse-animation';
            document.head.appendChild(pulseStyle);
        }
    }

    /**
     * Handle disease prediction link clicks
     */
    function setupLinkHandlers() {
        document.addEventListener('click', async (event) => {
            const link = event.target.closest(`
                a[href*="crop-disease"], 
                a[href*="disease"], 
                a[href*="127.0.0.1:5000"],
                [data-service="disease-prediction"]
            `);

            if (!link) return;

            const isDiseaseLink = link.href.includes('crop-disease') || 
                                 link.href.includes('127.0.0.1:5000') ||
                                 link.dataset.service === 'disease-prediction';

            if (isDiseaseLink) {
                event.preventDefault();
                
                const isRunning = await checkFlaskService();
                
                if (isRunning) {
                    // Service is running, open it
                    window.open(CONFIG.flaskUrl, '_blank');
                } else {
                    // Service not running, try to start it
                    showStatusNotification('Starting AI Disease Prediction Service...', 'info', 0);
                    
                    const started = await startFlaskViaManager();
                    
                    if (started) {
                        // Wait for service to be ready
                        showStatusNotification('Service starting, please wait...', 'info', 3000);
                        
                        setTimeout(async () => {
                            const ready = await checkFlaskService();
                            if (ready) {
                                showStatusNotification('AI Service Ready!', 'success');
                                setTimeout(() => {
                                    window.open(CONFIG.flaskUrl, '_blank');
                                }, 1000);
                            } else {
                                showManualStartGuidance();
                            }
                        }, 5000);
                    } else {
                        showManualStartGuidance();
                    }
                }
            }
        });
    }

    /**
     * Show manual start guidance
     */
    function showManualStartGuidance() {
        const guidance = document.createElement('div');
        guidance.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            z-index: 10001;
            font-family: 'Open Sans', sans-serif;
            max-width: 500px;
            text-align: center;
        `;

        guidance.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h3 style="color: #1f2937; margin-bottom: 15px;">🚀 Start AI Disease Prediction</h3>
                <p style="color: #6b7280; margin-bottom: 20px;">
                    Please start the KrishiVaani service to enable AI-powered disease prediction.
                </p>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; text-align: left; margin-bottom: 20px;">
                    <h4 style="color: #374151; margin: 0 0 15px 0;">Quick Start Options:</h4>
                    
                    <div style="margin-bottom: 15px;">
                        <strong>🖱️ Double-click:</strong><br>
                        <code style="background: #e5e7eb; padding: 4px 8px; border-radius: 4px; font-size: 13px;">start_krishivaani.bat</code>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <strong>💻 Command line:</strong><br>
                        <code style="background: #e5e7eb; padding: 4px 8px; border-radius: 4px; font-size: 13px;">python enhanced_krishivaani_manager.py</code>
                    </div>
                </div>
                
                <p style="font-size: 14px; color: #6b7280;">
                    After starting, return here and click the Disease Prediction link again.
                </p>
            </div>
            
            <div style="display: flex; gap: 10px; justify-content: center;">
                <button onclick="this.parentElement.parentElement.parentElement.remove()" style="
                    background: #3b82f6; color: white; border: none; padding: 10px 20px; 
                    border-radius: 6px; cursor: pointer; font-weight: 500;
                ">Got it!</button>
            </div>
        `;

        // Add backdrop
        const backdrop = document.createElement('div');
        backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 10000;
        `;
        backdrop.onclick = () => {
            backdrop.remove();
            guidance.remove();
        };

        document.body.appendChild(backdrop);
        document.body.appendChild(guidance);
    }

    /**
     * Try to auto-start Flask service
     */
    async function attemptAutoStart() {
        if (isStarting || startupAttempts >= CONFIG.maxRetries) return;

        isStarting = true;
        startupAttempts++;

        console.log(`🌱 Attempting to auto-start Flask service (attempt ${startupAttempts}/${CONFIG.maxRetries})`);

        // First try to run Start_Disease_Prediction.bat
        let started = await startFlaskViaBatch();
        
        // If batch method fails, try HTTP manager
        if (!started) {
            started = await startFlaskViaManager();
        }
        
        if (started) {
            console.log('✅ Flask service auto-start successful');
            showStatusNotification('AI Service Started Automatically!', 'success');
            
            // Wait and verify
            setTimeout(async () => {
                const running = await checkFlaskService();
                updateServiceIndicators(running);
            }, 3000);
        } else {
            console.log('⚠️ Flask service auto-start failed');
            if (startupAttempts === 1) {
                showStatusNotification('AI Service not running - click Disease Prediction for setup', 'info', 6000);
            }
        }

        isStarting = false;
    }

    /**
     * Monitor service status
     */
    async function monitorService() {
        const isRunning = await checkFlaskService();
        updateServiceIndicators(isRunning);
        
        // Auto-start if not running and haven't exceeded retries
        if (!isRunning && startupAttempts < CONFIG.maxRetries && !isStarting) {
            setTimeout(attemptAutoStart, 1000);
        }
    }

    /**
     * Initialize the auto-start system
     */
    function initialize() {
        console.log('🌾 KrishiVaani Flask Auto-Start initialized');
        
        // Setup link handlers
        setupLinkHandlers();
        
        // Initial service check and auto-start attempt
        setTimeout(monitorService, CONFIG.startupDelay);
        
        // Periodic monitoring
        serviceChecker = setInterval(monitorService, CONFIG.checkInterval);
        
        // Add global helper
        window.checkFlaskService = checkFlaskService;
        window.startFlaskService = attemptAutoStart;
    }

    /**
     * Cleanup
     */
    function cleanup() {
        if (serviceChecker) {
            clearInterval(serviceChecker);
            serviceChecker = null;
        }
        
        // Remove indicators
        document.querySelectorAll('.service-status-indicator').forEach(el => el.remove());
        document.querySelectorAll('.flask-auto-notification').forEach(el => el.remove());
        
        console.log('🧹 Flask Auto-Start cleaned up');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        setTimeout(initialize, 100);
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', cleanup);

    // Export for debugging
    window.flaskAutoStart = {
        checkService: checkFlaskService,
        startService: attemptAutoStart,
        showGuidance: showManualStartGuidance,
        cleanup: cleanup
    };

})();