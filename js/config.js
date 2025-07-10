
// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://0.0.0.0:8000/api',
    ENDPOINTS: {
        LOGIN: '/accounts/login/',
        REGISTER: '/accounts/register/',
        PROFILE: '/accounts/profile/',
        ELECTIONS: '/elections/',
        CANDIDATES: '/elections/candidates/',
        VOTE: '/voting/vote/',
        NOTIFICATIONS: '/notifications/',
        ADMIN: '/admin/'
    },
    HEADERS: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    }
};

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Storage helper functions
const Storage = {
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    get: (key) => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    },
    remove: (key) => localStorage.removeItem(key),
    clear: () => localStorage.clear()
};

export { API_CONFIG, Storage };
