// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";

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

// Password Toggle Functionality
function initializePasswordToggle() {
    const togglePasswordBtn = document.getElementById('togglePasswordBtn');
    const passwordInput = document.getElementById('password');
    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    
    console.log('Initializing password toggle...');
    console.log('Elements found:', {
        button: !!togglePasswordBtn,
        input: !!passwordInput,
        icon: !!togglePasswordIcon
    });
    
    if (togglePasswordBtn && passwordInput && togglePasswordIcon) {
        togglePasswordBtn.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            
            console.log('Toggle clicked - current type:', passwordInput.type);
            
            if (passwordInput.type === 'password') {
                // Show password
                passwordInput.type = 'text';
                togglePasswordIcon.classList.remove('fa-eye');
                togglePasswordIcon.classList.add('fa-eye-slash');
                togglePasswordBtn.classList.add('active');
                togglePasswordBtn.title = 'Hide Password';
                console.log('Password is now visible');
            } else {
                // Hide password
                passwordInput.type = 'password';
                togglePasswordIcon.classList.remove('fa-eye-slash');
                togglePasswordIcon.classList.add('fa-eye');
                togglePasswordBtn.classList.remove('active');
                togglePasswordBtn.title = 'Show Password';
                console.log('Password is now hidden');
            }
        });
        
        console.log('Password toggle initialized successfully!');
    } else {
        console.error('Could not find required elements for password toggle');
    }
}

// Initialize password toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing password toggle...');
    initializePasswordToggle();
});

// Also try when window is fully loaded as backup
window.addEventListener('load', function() {
    console.log('Window loaded, backup initialization...');
    // Small delay to ensure everything is rendered
    setTimeout(initializePasswordToggle, 100);
});

// inputs


// button
const login = document.getElementById('loginButton');
login.addEventListener("click", function (event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Show loading animation
    Swal.fire({
        title: '🔐 Authenticating...',
        html: '<p style="font-size: 16px; color: #6b7280;">Please wait while we verify your credentials</p>',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        customClass: 'enhanced-pulse',
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;
            
            // Store user info in localStorage for easy access
            localStorage.setItem('user', JSON.stringify({
                uid: user.uid,
                email: user.email,
                displayName: user.displayName || user.email
            }));
            
            // Enhanced success alert
            Swal.fire({
                title: '🎉 Login Successful!',
                html: '<p style="font-size: 16px; color: #6b7280; margin: 15px 0;">Welcome back to KrishiVaani! 🌱<br>Redirecting to your dashboard...</p>',
                icon: 'success',
                timer: 2500,
                timerProgressBar: true,
                showConfirmButton: false,
                allowOutsideClick: false,
                customClass: 'enhanced-bounce',
                background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
                color: '#166534',
                iconColor: '#22c55e'
            }).then(() => {
                // Mark that user has logged in successfully for location tracking
                localStorage.setItem('userLoggedIn', 'true');
                localStorage.setItem('loginTimestamp', new Date().toISOString());
                window.location.href = "dashboard.html";
            });
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            
            // Modern error alert
            let friendlyMessage = "Login failed. Please try again.";
            
            // Customize error messages
            if (errorCode === 'auth/user-not-found') {
                friendlyMessage = "No account found with this email address.";
            } else if (errorCode === 'auth/wrong-password') {
                friendlyMessage = "Incorrect password. Please try again.";
            } else if (errorCode === 'auth/invalid-email') {
                friendlyMessage = "Please enter a valid email address.";
            } else if (errorCode === 'auth/too-many-requests') {
                friendlyMessage = "Too many failed attempts. Please try again later.";
            }
            
            Swal.fire({
                title: '❌ Login Failed',
                html: `<p style="font-size: 16px; color: #6b7280; margin: 15px 0;">${friendlyMessage}</p>`,
                icon: 'error',
                confirmButtonText: '🔄 Try Again',
                confirmButtonColor: '#ef4444',
                customClass: 'enhanced-shake',
                background: 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
                color: '#991b1b',
                iconColor: '#ef4444',
                focusConfirm: true
            });
        });
})