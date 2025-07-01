import os
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"user_files/{filename}"

class SharedFile(models.Model):
    ALLOWED_EXTENSIONS = ['pptx', 'docx', 'xlsx']
    
    file = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(default=timezone.now)
    original_filename = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.original_filename} (Uploaded by {self.uploader.username})"

class FileShareLink(models.Model):
    file = models.ForeignKey(SharedFile, on_delete=models.CASCADE, related_name='share_links')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Share link for {self.file.original_filename}"