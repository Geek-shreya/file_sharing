from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('OPS', 'Operations User'),
        ('CLIENT', 'Client User'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.verification_token and self.user_type == 'CLIENT':
            self.verification_token = get_random_string(50)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"