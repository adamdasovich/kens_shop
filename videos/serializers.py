from rest_framework import serializers
from .models import Video, VideoCategory

class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = ('id', 'name', 'description')

class VideoSerializer(serializers.ModelSerializer):
    category = VideoCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'category', 'category_id', 'video_file', 
                 'thumbnail', 'duration', 'views', 'featured', 'created_at', 'updated_at')
class VideoListSerializer(serializers.ModelSerializer):
    category = VideoCategorySerializer(read_only=True)

    class Meta:
        model = Video
        fields =('id', 'title', 'thumbnail', 'duration', 'views', 'featured', 'category', 'created_at')
        