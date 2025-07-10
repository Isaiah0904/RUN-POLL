
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('election_created', 'Election Created'),
        ('election_started', 'Election Started'),
        ('election_ended', 'Election Ended'),
        ('registration_approved', 'Registration Approved'),
        ('registration_rejected', 'Registration Rejected'),
        ('candidate_approved', 'Candidate Approved'),
        ('candidate_rejected', 'Candidate Rejected'),
        ('vote_confirmation', 'Vote Confirmation'),
        ('system_announcement', 'System Announcement'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    action_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"

class SystemAnnouncement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    target_user_type = models.CharField(max_length=20, choices=[
        ('all', 'All Users'),
        ('voter', 'Voters'),
        ('admin', 'Administrators'),
    ], default='all')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
