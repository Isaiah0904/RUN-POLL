
// Utility functions
function showMessage(message, type) {
    // Create a simple alert for now
    alert(message);
}

function redirectBasedOnUserType() {
    const userType = localStorage.getItem('user_type');
    if (userType === 'admin') {
        window.location.href = '/admin-dashboard/';
    } else if (userType === 'voter') {
        window.location.href = '/voter-dashboard/';
    } else {
        window.location.href = '/';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const toggleOptions = document.querySelectorAll('.toggle-option');
    const toggleSlider = document.querySelector('.toggle-slider');
    const loginContainer = document.querySelector('.login-container');
    const loginImage = document.querySelector('.login-image');
    const loginButton = document.querySelector('.btn-login');

    let currentMode = 'voter';

    // Handle mode toggle
    toggleOptions.forEach(option => {
        option.addEventListener('click', function() {
            const mode = this.dataset.mode;
            currentMode = mode;
            
            // Update toggle appearance
            toggleOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            
            // Move slider
            if (mode === 'admin') {
                toggleSlider.classList.add('admin');
            } else {
                toggleSlider.classList.remove('admin');
            }
            
            // Update container classes
            if (mode === 'admin') {
                loginContainer.classList.add('admin-mode');
                loginImage.classList.add('admin-mode');
                loginButton.classList.add('admin-mode');
            } else {
                loginContainer.classList.remove('admin-mode');
                loginImage.classList.remove('admin-mode');
                loginButton.classList.remove('admin-mode');
            }
        });
    });

    // Handle form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                loginButton.disabled = true;
                loginButton.textContent = 'Signing In...';
                
                const response = await fetch('/api/accounts/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                        user_type: currentMode
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Store authentication data
                    localStorage.setItem('auth_token', data.token);
                    localStorage.setItem('user_type', data.user_type);
                    localStorage.setItem('user_id', data.user_id);
                    
                    if (data.profile) {
                        localStorage.setItem('user_profile', JSON.stringify(data.profile));
                    }
                    
                    showMessage('Login successful!', 'success');
                    
                    // Redirect based on user type
                    setTimeout(() => {
                        redirectBasedOnUserType();
                    }, 1000);
                } else {
                    showMessage(data.message || 'Login failed. Please check your credentials.', 'danger');
                }
            } catch (error) {
                showMessage('Login failed. Please check your credentials.', 'danger');
                console.error('Login error:', error);
            } finally {
                loginButton.disabled = false;
                loginButton.textContent = 'Sign In';
            }
        });
    }

    // Password toggle functionality
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordField = document.getElementById('password');
    
    if (passwordToggle && passwordField) {
        passwordToggle.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.innerHTML = type === 'password' ? '👁️' : '🙈';
        });
    }
});
