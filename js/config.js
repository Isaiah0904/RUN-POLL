
// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://0.0.0.0:8000',
    ENDPOINTS: {
        LOGIN: '/accounts/api/login/',
        REGISTER: '/accounts/api/register/',
        PROFILE: '/accounts/api/profile/',
        LOGOUT: '/accounts/api/logout/',
        USER_INFO: '/accounts/api/user-info/',
        ELECTIONS: '/elections/api/',
        ELECTION_DETAIL: '/elections/api/',
        ELECTION_CANDIDATES: '/elections/api/{id}/candidates/',
        REGISTER_CANDIDATE: '/elections/api/register-candidate/',
        DASHBOARD_STATS: '/elections/api/dashboard-stats/',
        CAST_VOTE: '/voting/api/cast-vote/',
        MY_VOTES: '/voting/api/my-votes/',
        ELECTION_RESULTS: '/voting/api/results/',
        VOTING_ELIGIBILITY: '/voting/api/eligibility/',
        NOTIFICATIONS: '/notifications/api/',
        MARK_READ: '/notifications/api/{id}/read/',
        UNREAD_COUNT: '/notifications/api/unread-count/',
        ANNOUNCEMENTS: '/notifications/api/announcements/'
    },
    HEADERS: {
        'Content-Type': 'application/json'
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

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_CONFIG, Storage };
}
