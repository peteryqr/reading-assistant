from django.db import models
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.

class User(AbstractUser):
    upload_directory = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.upload_directory:
            self.upload_directory = f'uploads/{self.username}'
        super().save(*args, **kwargs)

        # Create the upload directory if it doesn't exist
        os.makedirs(os.path.join('media', self.upload_directory), exist_ok=True)

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Highlight(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='highlights')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()  # The highlighted text
    page_number = models.IntegerField()  # Page number where the highlight appears
    position_data = models.JSONField()  # Store coordinates and other positioning data
    color = models.CharField(max_length=20, default='yellow')  # Highlight color
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)  # Optional note for the highlight

    class Meta:
        ordering = ['page_number', 'created_at']
