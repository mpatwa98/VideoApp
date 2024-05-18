from django.db import models

class VideoProject(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'),('archived', 'Archived'),], default='active')
    created_on = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='videos/', blank=True)