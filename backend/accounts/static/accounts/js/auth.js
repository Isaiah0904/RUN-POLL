import { API_CONFIG, Storage } from './config.js';

class AuthManager {
    constructor() {
        this.token = Storage.get('authToken');
        this.user = Storage.get('currentUser');
    }

    async login(email, password, userType = 'voter') {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
                method: 'POST',
                headers: API_CONFIG.HEADERS,
                body: JSON.stringify({
                    email,
                    password,
                    user_type: userType
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                Storage.set('authToken', this.token);
                Storage.set('currentUser', this.user);
                return { success: true, data };
            } else {
                return { success: false, error: data.message || 'Login failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please try again.' };
        }
    }

    async logout() {
        this.token = null;
        this.user = null;
        Storage.clear();
        window.location.href = '/Login.html';
    }

    isAuthenticated() {
        return !!this.token;
    }

    getAuthHeaders() {
        return {
            ...API_CONFIG.HEADERS,
            'Authorization': `Bearer ${this.token}`
        };
    }

    getCurrentUser() {
        return this.user;
    }

    redirectToLogin() {
        if (!this.isAuthenticated()) {
            window.location.href = '/Login.html';
        }
    }
}

// Create global auth instance
const Auth = new AuthManager();

// Authentication utilities
function checkAuth() {
    const token = localStorage.getItem('auth_token');
    const userType = localStorage.getItem('user_type');

    if (!token) {
        window.location.href = 'Login.html';
        return false;
    }

    return { token, userType };
}

function requireAuth(requiredUserType = null) {
    const auth = checkAuth();
    if (!auth) return false;

    if (requiredUserType && auth.userType !== requiredUserType) {
        showMessage('Access denied. Insufficient permissions.', 'error');
        setTimeout(() => {
            if (auth.userType === 'admin') {
                window.location.href = 'admin-dashboard.html';
            } else {
                window.location.href = 'Voter-dashboard.html';
            }
        }, 2000);
        return false;
    }

    return true;
}

function redirectBasedOnUserType() {
    const userType = localStorage.getItem('user_type');
    if (userType === 'admin') {
        window.location.href = 'admin-dashboard.html';
    } else if (userType === 'voter') {
        window.location.href = 'Voter-dashboard.html';
    } else {
        window.location.href = 'Login.html';
    }
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    const publicPages = ['Login.html', 'index.html', 'registration.html', 'forgot-password.html'];
    const currentPage = window.location.pathname.split('/').pop();

    if (!publicPages.includes(currentPage) && !Auth.isAuthenticated()) {
        Auth.redirectToLogin();
    }
});

export { Auth };