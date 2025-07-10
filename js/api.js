
const API_BASE_URL = 'http://localhost:5000/api';

class VotingAPI {
    constructor() {
        this.token = localStorage.getItem('auth_token');
        this.userType = localStorage.getItem('user_type');
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Token ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Authentication
    async login(email, password, userType) {
        const response = await this.request('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ email, password, user_type: userType })
        });

        if (response.token) {
            this.token = response.token;
            this.userType = userType;
            localStorage.setItem('auth_token', response.token);
            localStorage.setItem('user_type', userType);
            localStorage.setItem('user_data', JSON.stringify(response.user));
        }

        return response;
    }

    async register(userData) {
        return await this.request('/auth/register/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async logout() {
        await this.request('/auth/logout/', { method: 'POST' });
        this.token = null;
        this.userType = null;
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_type');
        localStorage.removeItem('user_data');
    }

    async getProfile() {
        return await this.request('/auth/profile/');
    }

    async updateProfile(profileData) {
        return await this.request('/auth/profile/', {
            method: 'PUT',
            body: JSON.stringify(profileData)
        });
    }

    // Elections
    async getElections() {
        return await this.request('/elections/');
    }

    async getElection(id) {
        return await this.request(`/elections/${id}/`);
    }

    async createElection(electionData) {
        return await this.request('/elections/', {
            method: 'POST',
            body: JSON.stringify(electionData)
        });
    }

    async getElectionCandidates(id) {
        return await this.request(`/elections/${id}/candidates/`);
    }

    async registerCandidate(candidateData) {
        return await this.request('/elections/register-candidate/', {
            method: 'POST',
            body: JSON.stringify(candidateData)
        });
    }

    async getDashboardStats() {
        return await this.request('/elections/dashboard-stats/');
    }

    // Voting
    async checkVotingEligibility(electionId) {
        return await this.request(`/voting/eligibility/${electionId}/`);
    }

    async castVote(voteData) {
        return await this.request('/voting/cast-vote/', {
            method: 'POST',
            body: JSON.stringify(voteData)
        });
    }

    async getMyVotes(electionId = null) {
        const params = electionId ? `?election=${electionId}` : '';
        return await this.request(`/voting/my-votes/${params}`);
    }

    async getElectionResults(electionId) {
        return await this.request(`/voting/results/${electionId}/`);
    }

    // Notifications
    async getNotifications() {
        return await this.request('/notifications/');
    }

    async markNotificationRead(id) {
        return await this.request(`/notifications/${id}/read/`, {
            method: 'PUT'
        });
    }

    async getUnreadCount() {
        return await this.request('/notifications/unread-count/');
    }

    async getAnnouncements() {
        return await this.request('/notifications/announcements/');
    }

    // Utility methods
    isAuthenticated() {
        return !!this.token;
    }

    isAdmin() {
        return this.userType === 'admin';
    }

    isVoter() {
        return this.userType === 'voter';
    }

    getCurrentUser() {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    }
}

// Global API instance
const api = new VotingAPI();

// Helper functions for common UI operations
function showMessage(message, type = 'info') {
    // Create or update message display
    const messageDiv = document.getElementById('message-display') || createMessageDisplay();
    messageDiv.className = `alert alert-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

function createMessageDisplay() {
    const div = document.createElement('div');
    div.id = 'message-display';
    div.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        padding: 15px;
        border-radius: 5px;
        max-width: 300px;
        display: none;
    `;
    document.body.appendChild(div);
    return div;
}

function redirectIfNotAuthenticated() {
    if (!api.isAuthenticated()) {
        window.location.href = 'Login.html';
        return false;
    }
    return true;
}

function redirectBasedOnUserType() {
    if (api.isAdmin()) {
        window.location.href = 'admin-dashboard.html';
    } else if (api.isVoter()) {
        window.location.href = 'Voter-dashboard.html';
    }
}
