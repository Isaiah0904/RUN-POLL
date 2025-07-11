
// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://0.0.0.0:8000/api',
    ENDPOINTS: {
        LOGIN: '/accounts/login/',
        REGISTER: '/accounts/register/',
        PROFILE: '/accounts/profile/',
        LOGOUT: '/accounts/logout/',
        ELECTIONS: '/elections/',
        ELECTION_DETAIL: '/elections/',
        ELECTION_CANDIDATES: '/elections/{id}/candidates/',
        REGISTER_CANDIDATE: '/elections/register-candidate/',
        DASHBOARD_STATS: '/elections/dashboard-stats/',
        CAST_VOTE: '/voting/cast-vote/',
        MY_VOTES: '/voting/my-votes/',
        ELECTION_RESULTS: '/voting/results/',
        VOTING_ELIGIBILITY: '/voting/eligibility/',
        NOTIFICATIONS: '/notifications/',
        MARK_READ: '/notifications/{id}/read/',
        UNREAD_COUNT: '/notifications/unread-count/',
        ANNOUNCEMENTS: '/notifications/announcements/'
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
