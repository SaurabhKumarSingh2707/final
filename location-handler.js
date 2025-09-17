// Live Location Handler for KrishiVaani
// This file provides live location functionality for the dashboard

class LocationHandler {
    constructor() {
        this.currentLocation = null;
        this.watchId = null;
        this.locationElement = null;
    }

    // Initialize location detection
    async initializeLocation() {
        // Check if geolocation is supported
        if (!navigator.geolocation) {
            console.error('Geolocation is not supported by this browser');
            this.displayLocationError('Geolocation not supported');
            return;
        }

        // Request location permission and get current position
        try {
            await this.getCurrentLocation();
            this.startLocationWatching();
        } catch (error) {
            console.error('Error getting location:', error);
            this.displayLocationError('Location access denied or failed');
        }
    }

    // Get current location once
    getCurrentLocation() {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.currentLocation = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        timestamp: new Date().toLocaleString()
                    };
                    
                    // Store location in localStorage for session persistence
                    localStorage.setItem('userLocation', JSON.stringify(this.currentLocation));
                    
                    this.displayLocation();
                    resolve(position);
                },
                (error) => {
                    // If permission denied, check if we have stored location
                    const storedLocation = localStorage.getItem('userLocation');
                    if (storedLocation) {
                        try {
                            this.currentLocation = JSON.parse(storedLocation);
                            // Update timestamp to show it's cached
                            this.currentLocation.timestamp = `${new Date().toLocaleString()} (cached)`;
                            this.displayLocation();
                            resolve({ coords: this.currentLocation });
                            return;
                        } catch (e) {
                            console.error('Error parsing stored location:', e);
                        }
                    }
                    reject(error);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000 // 5 minutes
                }
            );
        });
    }

    // Start watching location changes
    startLocationWatching() {
        if (navigator.geolocation) {
            this.watchId = navigator.geolocation.watchPosition(
                (position) => {
                    this.currentLocation = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        timestamp: new Date().toLocaleString()
                    };
                    this.displayLocation();
                },
                (error) => {
                    console.error('Error watching location:', error);
                    this.displayLocationError('Unable to track location');
                },
                {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 300000 // 5 minutes
                }
            );
        }
    }

    // Stop watching location
    stopLocationWatching() {
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
    }

    // Display current location
    async displayLocation() {
        const locationElement = document.getElementById('user-location');
        if (!locationElement || !this.currentLocation) return;

        const { latitude, longitude, timestamp } = this.currentLocation;
        
        try {
            // Get human-readable address using reverse geocoding
            const address = await this.reverseGeocode(latitude, longitude);
            
            locationElement.innerHTML = `
                <div class="location-info">
                    <div class="location-header">
                        <i class="fas fa-map-marker-alt location-icon"></i>
                        <span class="location-title">Your Location</span>
                        <span class="location-status online">Live</span>
                    </div>
                    <div class="location-details">
                        <div class="location-address">${address}</div>
                    </div>
                </div>
            `;
            
            // Add animation class
            locationElement.classList.add('location-updated');
            setTimeout(() => {
                locationElement.classList.remove('location-updated');
            }, 500);
            
        } catch (error) {
            console.error('Error getting address:', error);
            locationElement.innerHTML = `
                <div class="location-info">
                    <div class="location-header">
                        <i class="fas fa-map-marker-alt location-icon"></i>
                        <span class="location-title">Your Location</span>
                        <span class="location-status online">Live</span>
                    </div>
                    <div class="location-details">
                        <div class="location-address">Location detected</div>
                    </div>
                </div>
            `;
        }
    }

    // Display location error
    displayLocationError(message) {
        const locationElement = document.getElementById('user-location');
        if (!locationElement) return;

        locationElement.innerHTML = `
            <div class="location-info error">
                <div class="location-header">
                    <i class="fas fa-exclamation-triangle location-icon"></i>
                    <span class="location-title">Location Unavailable</span>
                    <span class="location-status offline">Offline</span>
                </div>
                <div class="location-details">
                    <div class="location-error">${message}</div>
                    <button class="retry-location-btn" onclick="locationHandler.initializeLocation()">
                        <i class="fas fa-redo"></i> Retry
                    </button>
                </div>
            </div>
        `;
    }

    // Reverse geocoding to get human-readable address
    async reverseGeocode(latitude, longitude) {
        try {
            // Using OpenStreetMap Nominatim API (free, no API key required)
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=18&addressdetails=1`
            );
            
            if (!response.ok) throw new Error('Geocoding failed');
            
            const data = await response.json();
            
            if (data && data.display_name) {
                // Extract district and state information
                const address = data.address || {};
                const locationParts = [];
                
                // Add district information
                if (address.state_district) {
                    locationParts.push(address.state_district);
                } else if (address.county) {
                    locationParts.push(address.county);
                } else if (address.city_district) {
                    locationParts.push(address.city_district);
                } else if (address.city || address.town) {
                    locationParts.push(address.city || address.town);
                }
                
                // Add state
                if (address.state) {
                    locationParts.push(address.state);
                }
                
                // Return formatted location string (District, State)
                if (locationParts.length > 0) {
                    return locationParts.join(', ');
                }
                
                // Fallback to display name parsing if structured data not available
                const fallbackParts = data.display_name.split(',').slice(-3, -1).map(part => part.trim());
                return fallbackParts.join(', ');
            }
            
            return `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
        } catch (error) {
            console.error('Reverse geocoding failed:', error);
            return `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
        }
    }

    // Get weather info for current location (optional enhancement)
    async getLocationWeather() {
        if (!this.currentLocation) return null;
        
        // This would integrate with weather API
        // For now, return null - can be enhanced later
        return null;
    }
}

// Create global instance
const locationHandler = new LocationHandler();

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit for other elements to load, then initialize location
    setTimeout(() => {
        locationHandler.initializeLocation();
    }, 1000);
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    locationHandler.stopLocationWatching();
});