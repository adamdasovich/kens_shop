from django.contrib import admin
from .models import *

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'content_short', 'parent', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'content_type', 'created_at')
    search_fields = ('user__username', 'content')
    list_editable = ('is_approved',)
    ordering = ('-created_at',)
    
    def content_short(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_short.short_description = 'Content'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'rating', 'created_at')
    list_filter = ('rating', 'content_type', 'created_at')
    search_fields = ('user__username', 'review')
    ordering = ('-created_at',)