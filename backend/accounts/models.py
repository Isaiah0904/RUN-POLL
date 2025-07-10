
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    USER_TYPES = (
        ('voter', 'Voter'),
        ('admin', 'Administrator'),
        ('candidate', 'Candidate'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='voter')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class VoterProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Engineering', 'Engineering'),
        ('Business', 'Business'),
        ('Arts', 'Arts'),
        ('Sciences', 'Sciences'),
        ('Medicine', 'Medicine'),
        ('Law', 'Law'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_eligible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='System Administrator')
    department = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='admin_profiles/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
