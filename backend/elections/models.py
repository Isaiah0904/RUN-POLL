
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Election(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('immediate', 'Immediate'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    results_visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    eligible_departments = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_elections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.status == 'ongoing'
    
    @property
    def total_votes(self):
        return sum(position.total_votes for position in self.positions.all())
    
    def update_status(self):
        now = timezone.now()
        if now < self.start_date:
            self.status = 'upcoming'
        elif self.start_date <= now <= self.end_date:
            self.status = 'ongoing'
        elif now > self.end_date:
            self.status = 'completed'
        self.save()

class Position(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    max_candidates = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"{self.title} - {self.election.title}"
    
    @property
    def total_votes(self):
        return sum(candidate.vote_count for candidate in self.candidates.all())

class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidacies')
    manifesto = models.TextField()
    profile_image = models.ImageField(upload_to='candidate_images/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['position', 'user']
    
    def __str__(self):
        return f"{self.user.username} for {self.position.title}"
    
    @property
    def vote_count(self):
        from voting.models import Vote
        return Vote.objects.filter(candidate=self).count()
    
    @property
    def vote_percentage(self):
        total_votes = self.position.total_votes
        if total_votes == 0:
            return 0
        return round((self.vote_count / total_votes) * 100, 2)

class ElectionRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='election_registrations')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registration_date = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_registrations')
    
    class Meta:
        unique_together = ['voter', 'election']
    
    def __str__(self):
        return f"{self.voter.username} - {self.election.title} ({self.status})"
