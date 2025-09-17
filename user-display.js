// User Authentication Handler for Dashboard
// This file handles user authentication state and displays user information

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyBzgNpV6aFyjtDX6Ig9rgP8x2w647jWN5M",
    authDomain: "smart-crop-advisory-f3913.firebaseapp.com",
    projectId: "smart-crop-advisory-f3913",
    storageBucket: "smart-crop-advisory-f3913.firebasestorage.app",
    messagingSenderId: "231721730375",
    appId: "1:231721730375:web:a07c0b372e8b99ed27cc62"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();

class UserDisplayHandler {
    constructor() {
        this.currentUser = null;
        this.userEmailElement = null;
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupUserDisplay());
        } else {
            this.setupUserDisplay();
        }
    }

    setupUserDisplay() {
        this.userEmailElement = document.getElementById('userEmailText');
        
        // Listen for authentication state changes
        onAuthStateChanged(auth, (user) => {
            if (user) {
                this.currentUser = user;
                this.displayUserInfo(user);
            } else {
                // User is signed out, redirect to login
                console.log('User not authenticated, redirecting to login...');
                window.location.href = 'login.html';
            }
        });
    }

    displayUserInfo(user) {
        if (!this.userEmailElement) {
            this.userEmailElement = document.getElementById('userEmailText');
        }

        if (this.userEmailElement && user) {
            // Extract username from email (part before @)
            const email = user.email;
            const username = email.split('@')[0];
            
            // Display the full email with nice formatting
            this.userEmailElement.textContent = email;
            this.userEmailElement.title = `Logged in as: ${email}`;
            
            // Store user info in localStorage for other components
            localStorage.setItem('currentUser', JSON.stringify({
                email: user.email,
                uid: user.uid,
                displayName: user.displayName || username,
                photoURL: user.photoURL
            }));

            // Add loading animation removal
            const emailDisplay = document.getElementById('userEmailDisplay');
            if (emailDisplay) {
                emailDisplay.classList.add('loaded');
                setTimeout(() => {
                    emailDisplay.classList.remove('loaded');
                }, 300);
            }
        }
    }

    getCurrentUser() {
        return this.currentUser;
    }

    getUserEmail() {
        return this.currentUser ? this.currentUser.email : null;
    }

    getUserDisplayName() {
        if (!this.currentUser) return null;
        
        const email = this.currentUser.email;
        return this.currentUser.displayName || email.split('@')[0];
    }
}

// Create global instance
const userDisplayHandler = new UserDisplayHandler();

// Make it globally available
window.userDisplayHandler = userDisplayHandler;