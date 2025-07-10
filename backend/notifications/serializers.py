
from rest_framework import serializers
from .models import Notification, SystemAnnouncement

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 
                 'created_at', 'action_url']
        read_only_fields = ['created_at']

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.admin_profile.first_name', read_only=True)
    
    class Meta:
        model = SystemAnnouncement
        fields = ['id', 'title', 'content', 'priority', 'target_user_type', 
                 'is_active', 'created_at', 'expires_at', 'created_by_name']
        read_only_fields = ['created_at', 'created_by_name']
