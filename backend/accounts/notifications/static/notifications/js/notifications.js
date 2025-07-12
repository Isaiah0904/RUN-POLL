
import { API_CONFIG } from './config.js';
import { Auth } from './auth.js';

class NotificationManager {
    constructor() {
        this.notifications = [];
        this.unreadCount = 0;
    }

    async fetchNotifications() {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.NOTIFICATIONS}`, {
                headers: Auth.getAuthHeaders()
            });
            const data = await response.json();
            this.notifications = data.results || [];
            this.updateUnreadCount();
            return this.notifications;
        } catch (error) {
            console.error('Error fetching notifications:', error);
            return [];
        }
    }

    async markAsRead(notificationId) {
        try {
            const response = await fetch(`${API_CONFIG.BASE_URL}/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: Auth.getAuthHeaders()
            });
            
            if (response.ok) {
                const notification = this.notifications.find(n => n.id === notificationId);
                if (notification) {
                    notification.is_read = true;
                    this.updateUnreadCount();
                }
                return { success: true };
            }
            return { success: false };
        } catch (error) {
            console.error('Error marking notification as read:', error);
            return { success: false };
        }
    }

    updateUnreadCount() {
        this.unreadCount = this.notifications.filter(n => !n.is_read).length;
        this.updateBadge();
    }

    updateBadge() {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            if (this.unreadCount > 0) {
                badge.textContent = this.unreadCount;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    showToast(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="bi bi-${this.getIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Hide toast after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }

    getIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'x-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
}

export { NotificationManager };
