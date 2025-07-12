
import { API_CONFIG, Storage } from './config.js';
import { Auth } from './auth.js';

class ElectionManager {
    async getElections() {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ELECTIONS}`, {
                headers: Auth.getAuthHeaders()
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching elections:', error);
            return [];
        }
    }

    async getElectionCandidates(electionId) {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/elections/${electionId}/candidates/`, {
                headers: Auth.getAuthHeaders()
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching candidates:', error);
            return [];
        }
    }

    async registerForElection(electionId) {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/elections/${electionId}/register/`, {
                method: 'POST',
                headers: Auth.getAuthHeaders()
            });
            return await response.json();
        } catch (error) {
            console.error('Error registering for election:', error);
            return { success: false, error: 'Registration failed' };
        }
    }

    async submitVote(voteData) {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.VOTE}`, {
                method: 'POST',
                headers: Auth.getAuthHeaders(),
                body: JSON.stringify(voteData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error submitting vote:', error);
            return { success: false, error: 'Vote submission failed' };
        }
    }

    async getElectionResults(electionId) {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/elections/${electionId}/results/`, {
                headers: Auth.getAuthHeaders()
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching results:', error);
            return [];
        }
    }
}

export { ElectionManager };
