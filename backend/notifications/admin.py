
from django.contrib import admin
from .models import Notification, SystemAnnouncement

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'recipient__username', 'message']
    readonly_fields = ['created_at']

@admin.register(SystemAnnouncement)
class SystemAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'target_user_type', 'is_active', 'created_at', 'expires_at']
    list_filter = ['priority', 'target_user_type', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new announcement
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
