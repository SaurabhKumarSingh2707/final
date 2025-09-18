// Contact Form JavaScript with Firebase Integration

// Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyBzgNpV6aFyjtDX6Ig9rgP8x2w647jWN5M",
  authDomain: "smart-crop-advisory-f3913.firebaseapp.com",
  databaseURL: "https://smart-crop-advisory-f3913-default-rtdb.firebaseio.com",
  projectId: "smart-crop-advisory-f3913",
  storageBucket: "smart-crop-advisory-f3913.firebasestorage.app",
  messagingSenderId: "231721730375",
  appId: "1:231721730375:web:a07c0b372e8b99ed27cc62"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Get a reference to the database service
const database = firebase.database();
const messagesRef = database.ref('contactMessages');

// Theme toggle functionality
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    const themeText = document.querySelector('.theme-text');
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        themeIcon.classList.replace('fa-moon', 'fa-sun');
        themeText.textContent = 'Light';
        window.currentTheme = 'light';
    } else {
        body.classList.add('dark-theme');
        themeIcon.classList.replace('fa-sun', 'fa-moon');
        themeText.textContent = 'Dark';
        window.currentTheme = 'dark';
    }
}

// Load theme on page load
function loadTheme() {
    const themeIcon = document.querySelector('.theme-icon');
    const themeText = document.querySelector('.theme-text');
    
    if (window.currentTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeIcon.classList.replace('fa-sun', 'fa-moon');
        themeText.textContent = 'Dark';
    }
}

// Wait for DOM and Firebase to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing form...');
    
    // Load theme
    loadTheme();
    
    // Get form elements
    const feedbackForm = document.getElementById('feedbackForm');
    const thankYouMessage = document.getElementById('thankYouMessage');
    const allFeedbacksSection = document.getElementById('allFeedbacks');
    const feedbacksList = document.getElementById('feedbacksList');
    const feedbackTextarea = document.getElementById('feedback');
    const charCountElement = document.getElementById('charCount');

    // Character count functionality
    if (feedbackTextarea && charCountElement) {
        feedbackTextarea.addEventListener('input', function() {
            const charCount = this.value.length;
            charCountElement.textContent = charCount;
            
            if (charCount > 500) {
                charCountElement.style.color = '#ff7043';
            } else if (charCount > 300) {
                charCountElement.style.color = '#ff9800';
            } else {
                charCountElement.style.color = '#81c784';
            }
        });
    }

    // Phone number formatting
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value.length <= 10) {
                    value = value.replace(/(\d{5})(\d{5})/, '$1 $2');
                } else if (value.length <= 12) {
                    value = '+' + value.substring(0, 2) + ' ' + value.substring(2, 7) + ' ' + value.substring(7);
                }
            }
            e.target.value = value;
        });
    }

    // Form submission handler
    if (feedbackForm) {
        console.log('Form found, adding event listener...');
        
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Form submitted, processing...');
            
            // Get form values using getInputVal function
            const name = getInputVal('name');
            const email = getInputVal('email');
            const phone = getInputVal('phone');
            const feedback = getInputVal('feedback');
            
            console.log('Form data:', { name, email, phone, feedback });
            
            // Validate required fields
            if (!name || !email || !feedback) {
                Swal.fire({
                    title: 'Missing Required Information',
                    text: 'Please fill in all required fields (Name, Email, and Message).',
                    icon: 'warning',
                    confirmButtonColor: '#4caf50'
                });
                return;
            }
            
            // Validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                Swal.fire({
                    title: 'Invalid Email',
                    text: 'Please enter a valid email address.',
                    icon: 'warning',
                    confirmButtonColor: '#4caf50'
                });
                return;
            }
            
            const submitButton = this.querySelector('.submit-button');
            const originalText = submitButton.innerHTML;
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Submitting...</span>';
            submitButton.disabled = true;
            
            // Save message to Firebase
            saveMessage(name, email, phone, feedback);
        });
    } else {
        console.error('Form not found!');
    }
});

// Function to get form input values
function getInputVal(id) {
    const element = document.getElementById(id);
    return element ? element.value.trim() : '';
}

// Save message to Firebase
function saveMessage(name, email, phone, message) {
    console.log('Saving to Firebase:', { name, email, phone, message });
    
    // Create new message reference
    const newMessageRef = messagesRef.push();
    
    // Data to save
    const messageData = {
        name: name,
        email: email,
        phone: phone || null,
        message: message,
        timestamp: firebase.database.ServerValue.TIMESTAMP,
        dateCreated: new Date().toISOString(),
        dateFormatted: new Date().toLocaleString()
    };
    
    console.log('Message data to save:', messageData);
    
    // Save to Firebase
    newMessageRef.set(messageData)
        .then(() => {
            console.log('Message saved successfully to Firebase!');
            
            // Reset form
            document.getElementById('feedbackForm').reset();
            
            // Reset character count
            const charCountElement = document.getElementById('charCount');
            if (charCountElement) {
                charCountElement.textContent = '0';
                charCountElement.style.color = '#81c784';
            }
            
            // Reset submit button
            const submitButton = document.querySelector('.submit-button');
            submitButton.innerHTML = '<i class="fas fa-paper-plane"></i><span>Send Message</span>';
            submitButton.disabled = false;
            
            // Show success message
            Swal.fire({
                title: '✅ Sent!',
                text: 'We\'ll get back to you soon',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true,
                toast: true,
                position: 'top-end',
                background: '#f8fafc',
                color: '#0f172a',
                customClass: {
                    popup: 'minimal-toast',
                    timerProgressBar: 'minimal-progress'
                }
            }).then(() => {
                // Show thank you section
                const feedbackForm = document.getElementById('feedbackForm');
                const thankYouMessage = document.getElementById('thankYouMessage');
                const feedbackHeader = document.querySelector('.feedback-header');
                
                if (feedbackForm && thankYouMessage) {
                    feedbackForm.classList.add('hidden');
                    if (feedbackHeader) feedbackHeader.classList.add('hidden');
                    thankYouMessage.classList.remove('hidden');
                }
            });
        })
        .catch((error) => {
            console.error('Error saving message to Firebase:', error);
            
            // Reset submit button
            const submitButton = document.querySelector('.submit-button');
            submitButton.innerHTML = '<i class="fas fa-paper-plane"></i><span>Send Message</span>';
            submitButton.disabled = false;
            
            // Show error message
            Swal.fire({
                title: '❌ Failed to send',
                text: 'Please try again',
                showConfirmButton: false,
                timer: 2500,
                toast: true,
                position: 'top-end',
                background: '#fef2f2',
                color: '#991b1b',
                customClass: {
                    popup: 'minimal-toast-error'
                }
            });
        });
}

// Load messages from Firebase
function loadMessagesFromFirebase() {
    console.log('Loading messages from Firebase...');
    
    return messagesRef.orderByChild('timestamp').once('value')
        .then((snapshot) => {
            console.log('Firebase response received');
            const messages = [];
            
            snapshot.forEach((childSnapshot) => {
                const message = childSnapshot.val();
                message.id = childSnapshot.key;
                messages.unshift(message); // Add to beginning for newest first
            });
            
            console.log('Loaded messages:', messages);
            return messages;
        })
        .catch((error) => {
            console.error('Error loading messages:', error);
            throw error;
        });
}

// Helper function to get field labels
function getFieldLabel(fieldName) {
    const labels = {
        name: 'Full Name',
        email: 'Email Address',
        phone: 'Phone Number',
        feedback: 'Message Details'
    };
    return labels[fieldName] || fieldName;
}

// Show all contact messages
function showAllFeedbacks() {
    const thankYouMessage = document.getElementById('thankYouMessage');
    const allFeedbacksSection = document.getElementById('allFeedbacks');
    const feedbacksList = document.getElementById('feedbacksList');
    
    thankYouMessage.classList.add('hidden');
    allFeedbacksSection.classList.remove('hidden');
    
    // Show loading
    feedbacksList.innerHTML = `
        <div class="no-feedback">
            <i class="fas fa-spinner fa-spin" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.6;"></i>
            <p style="font-size: 1rem; margin-bottom: 0.5rem;">Loading messages...</p>
        </div>
    `;
    
    // Load messages from Firebase
    loadMessagesFromFirebase()
        .then((allFeedbacks) => {
            if (allFeedbacks.length === 0) {
                feedbacksList.innerHTML = `
                    <div class="no-feedback">
                        <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.6;"></i>
                        <p style="font-size: 1rem; margin-bottom: 0.5rem;">No contact messages yet</p>
                        <p style="font-size: 0.9rem; opacity: 0.8;">Be the first to get in touch!</p>
                    </div>
                `;
                return;
            }

            feedbacksList.innerHTML = allFeedbacks.map((fb, index) => `
                <div class="feedback-item">
                    <h4><i class="fas fa-user-circle" style="color: #4caf50; margin-right: 8px;"></i>${escapeHtml(fb.name || 'Anonymous')}</h4>
                    
                    <div style="margin: 10px 0; font-size: 0.9rem; color: #94a3b8;">
                        <div style="margin-bottom: 5px;"><i class="fas fa-envelope" style="margin-right: 8px; color: #66bb6a;"></i>${escapeHtml(fb.email || 'Not provided')}</div>
                        ${fb.phone ? `<div><i class="fas fa-phone" style="margin-right: 8px; color: #66bb6a;"></i>${escapeHtml(fb.phone)}</div>` : ''}
                    </div>
                    
                    <p style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(148, 163, 184, 0.2);"><i class="fas fa-quote-left" style="color: #66bb6a; margin-right: 8px; opacity: 0.6;"></i>${escapeHtml(fb.message || 'No message provided')}</p>
                    
                    <div class="feedback-meta">
                        📝 Message #${index + 1} • ${formatDate(fb.dateFormatted || fb.date)}
                    </div>
                </div>
            `).join('');
        })
        .catch((error) => {
            console.error('Error loading messages:', error);
            feedbacksList.innerHTML = `
                <div class="no-feedback">
                    <i class="fas fa-exclamation-triangle" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.6; color: #ff7043;"></i>
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;">Error loading messages</p>
                    <p style="font-size: 0.9rem; opacity: 0.8;">Please try again later.</p>
                </div>
            `;
        });
}

// Show new contact form
function showNewFeedbackForm() {
    const feedbackForm = document.getElementById('feedbackForm');
    const thankYouMessage = document.getElementById('thankYouMessage');
    const allFeedbacksSection = document.getElementById('allFeedbacks');
    const feedbackHeader = document.querySelector('.feedback-header');
    
    // Hide all sections
    thankYouMessage.classList.add('hidden');
    allFeedbacksSection.classList.add('hidden');
    
    // Show form
    feedbackForm.classList.remove('hidden');
    feedbackHeader.classList.remove('hidden');
    
    // Reset form
    feedbackForm.reset();
    const charCountElement = document.getElementById('charCount');
    if (charCountElement) {
        charCountElement.textContent = '0';
        charCountElement.style.color = '#81c784';
    }
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays <= 7) return `${diffDays - 1} days ago`;
    return date.toLocaleDateString();
}

// Logout confirmation
function showLogoutConfirmation() {
    Swal.fire({
        title: 'Confirm Logout',
        text: 'Are you sure you want to logout?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ff7043',
        cancelButtonColor: '#4caf50',
        confirmButtonText: 'Yes, logout',
        cancelButtonText: 'Cancel',
        customClass: {
            popup: 'swal-custom'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = 'index.html';  
        }
    });
}