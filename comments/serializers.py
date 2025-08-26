from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment, Rating

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'parent', 'replies', 'created_at', 'updated_at')
        read_only_fields = ('user', )

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
    

class CommentCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('content', 'content_type', 'object_id', 'parent')

    def validate_content_type(self, value):
        try:
            content_type = ContentType.objects.get(model=value.lower())
            return content_type
        except ContentType.DoesNotExist:
            raise serializers.ValidationError('Invalid content type')
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'rating', 'review', 'create_at', 'updated_at')
        read_only_fields = ('user',)

class RatingCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = Rating
        fields = ('content_type', 'object_id', 'rating', 'review')

    def validate_content_type(self, value):
        try:
            content_type = ContentType.objects.get(model=value.lower())
            return content_type
        except ContentType.DoesNotExist:
            raise serializers.ValidationError('Invalid content type')
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)