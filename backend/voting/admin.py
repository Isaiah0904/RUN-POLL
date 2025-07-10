
from django.contrib import admin
from .models import Vote, VotingSession

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'position', 'election', 'timestamp']
    list_filter = ['election', 'position', 'timestamp']
    search_fields = ['voter__username', 'candidate__user__username', 'election__title']
    readonly_fields = ['timestamp']

@admin.register(VotingSession)
class VotingSessionAdmin(admin.ModelAdmin):
    list_display = ['voter', 'election', 'start_time', 'end_time', 'is_completed', 'ip_address']
    list_filter = ['election', 'is_completed', 'start_time']
    search_fields = ['voter__username', 'election__title']
    readonly_fields = ['start_time', 'end_time']
