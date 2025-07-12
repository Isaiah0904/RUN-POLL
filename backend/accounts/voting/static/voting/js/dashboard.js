
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!redirectIfNotAuthenticated()) return;

    const currentUser = api.getCurrentUser();
    
    // Load dashboard based on user type
    if (api.isVoter()) {
        loadVoterDashboard();
    } else if (api.isAdmin()) {
        loadAdminDashboard();
    }

    // Load notifications
    loadNotifications();
});

async function loadVoterDashboard() {
    try {
        // Load active elections
        const elections = await api.getElections();
        const activeElections = elections.filter(election => election.status === 'active');
        
        displayActiveElections(activeElections);
        
        // Load my votes
        const myVotes = await api.getMyVotes();
        displayVotingHistory(myVotes);
        
    } catch (error) {
        showMessage('Error loading dashboard data', 'danger');
        console.error('Dashboard error:', error);
    }
}

async function loadAdminDashboard() {
    try {
        // Load dashboard statistics
        const stats = await api.getDashboardStats();
        displayDashboardStats(stats);
        
        // Load recent elections
        const elections = await api.getElections();
        displayRecentElections(elections);
        
    } catch (error) {
        showMessage('Error loading admin dashboard', 'danger');
        console.error('Admin dashboard error:', error);
    }
}

function displayActiveElections(elections) {
    const container = document.getElementById('active-elections');
    if (!container) return;
    
    if (elections.length === 0) {
        container.innerHTML = '<p>No active elections at this time.</p>';
        return;
    }
    
    const html = elections.map(election => `
        <div class="election-card">
            <h4>${election.title}</h4>
            <p>${election.description}</p>
            <p><strong>Ends:</strong> ${new Date(election.end_date).toLocaleDateString()}</p>
            <button onclick="viewElection(${election.id})" class="btn btn-primary">
                View Election
            </button>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function displayDashboardStats(stats) {
    // Update stat cards
    if (document.getElementById('total-elections')) {
        document.getElementById('total-elections').textContent = stats.total_elections || 0;
    }
    if (document.getElementById('active-elections')) {
        document.getElementById('active-elections').textContent = stats.active_elections || 0;
    }
    if (document.getElementById('total-voters')) {
        document.getElementById('total-voters').textContent = stats.total_voters || 0;
    }
    if (document.getElementById('total-votes')) {
        document.getElementById('total-votes').textContent = stats.total_votes || 0;
    }
}

async function loadNotifications() {
    try {
        const notifications = await api.getNotifications();
        const unreadCount = await api.getUnreadCount();
        
        displayNotifications(notifications);
        updateNotificationBadge(unreadCount.unread_count);
        
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

function displayNotifications(notifications) {
    const container = document.getElementById('notifications-list');
    if (!container) return;
    
    if (notifications.length === 0) {
        container.innerHTML = '<p>No notifications.</p>';
        return;
    }
    
    const html = notifications.slice(0, 5).map(notification => `
        <div class="notification-item ${notification.is_read ? '' : 'unread'}" 
             onclick="markAsRead(${notification.id})">
            <h6>${notification.title}</h6>
            <p>${notification.message}</p>
            <small>${new Date(notification.created_at).toLocaleDateString()}</small>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function updateNotificationBadge(count) {
    const badge = document.getElementById('notification-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
    }
}

async function markAsRead(notificationId) {
    try {
        await api.markNotificationRead(notificationId);
        loadNotifications(); // Refresh notifications
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

function viewElection(electionId) {
    window.location.href = `election-page.html?id=${electionId}`;
}

// Logout functionality
function logout() {
    api.logout().then(() => {
        window.location.href = 'Login.html';
    });
}
