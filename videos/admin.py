from django.contrib import admin
from .models import *

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'views', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('featured',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Media Files', {
            'fields': ('video_file', 'thumbnail')
        }),
        ('Metadata', {
            'fields': ('duration', 'featured', 'views', 'created_at', 'updated_at')
        }),
    )