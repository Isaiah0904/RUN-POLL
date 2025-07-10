
from django.db import models
from django.contrib.auth import get_user_model
from elections.models import Candidate, Position, Election

User = get_user_model()

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['voter', 'position', 'election']  # One vote per position per election
    
    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.user.username} in {self.position.title}"

class VotingSession(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voting_sessions')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voting_sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.voter.username} - {self.election.title} session"
