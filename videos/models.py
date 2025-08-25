from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Video Categories'

    def __str__(self):
        return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='videos/%Y/%m/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/%Y/%m/')
    duration = models.PositiveIntegerField(help_text='Duration in seconds')
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


