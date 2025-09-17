// Global Logout Handler for KrishiVaani
// This file provides a standardized logout functionality across all pages

// Function to show logout confirmation with enhanced styling
async function showLogoutConfirmation() {
    // Import Firebase auth functions dynamically
    const { getAuth, signOut } = await import("https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js");
    const auth = getAuth();
    
    Swal.fire({
        title: '👋 Confirm Logout',
        html: '<p style="font-size: 16px; color: #6b7280; margin: 15px 0;">Are you sure you want to logout from your account?</p>',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6b7280',
        confirmButtonText: '✅ Yes, logout',
        cancelButtonText: '❌ Cancel',
        customClass: {
            popup: 'enhanced-slide-down',
            confirmButton: 'enhanced-button',
            cancelButton: 'enhanced-button'
        },
        showClass: {
            backdrop: 'swal2-backdrop-show'
        },
        hideClass: {
            backdrop: 'swal2-backdrop-hide',
            popup: 'enhanced-zoom-out'
        },
        backdrop: true,
        focusCancel: true,
        reverseButtons: true
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                // Sign out from Firebase
                await signOut(auth);
                
                // Clear any stored user data/session
                localStorage.clear();
                sessionStorage.clear();
                
                // Show success message
                Swal.fire({
                    title: '✨ Successfully Logged Out!',
                    html: '<p style="font-size: 16px; color: #6b7280;">Thank you for using KrishiVaani. See you soon! 🌱</p>',
                    icon: 'success',
                    timer: 2500,
                    timerProgressBar: true,
                    showConfirmButton: false,
                    customClass: {
                        popup: 'enhanced-pulse'
                    },
                    showClass: {
                        backdrop: 'swal2-backdrop-show'
                    },
                    hideClass: {
                        backdrop: 'swal2-backdrop-hide',
                        popup: 'enhanced-zoom-out'
                    },
                    backdrop: true,
                    allowOutsideClick: false
                }).then(() => {
                    // Redirect to home page
                    window.location.href = 'index.html';
                });
            } catch (error) {
                console.error('Logout error:', error);
                Swal.fire({
                    title: '⚠️ Logout Failed',
                    html: '<p style="font-size: 16px; color: #6b7280;">Something went wrong. Please try again.</p>',
                    icon: 'error',
                    confirmButtonText: '🔄 Try Again',
                    confirmButtonColor: '#ef4444',
                    customClass: {
                        popup: 'enhanced-shake',
                        confirmButton: 'enhanced-button'
                    },
                    showClass: {
                        backdrop: 'swal2-backdrop-show'
                    },
                    hideClass: {
                        backdrop: 'swal2-backdrop-hide',
                        popup: 'enhanced-zoom-out'
                    },
                    backdrop: true
                });
            }
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            // Handle cancel button - redirect to dashboard
            window.location.href = 'dashboard.html';
        }
    });
}

// Make the function globally available
window.showLogoutConfirmation = showLogoutConfirmation;