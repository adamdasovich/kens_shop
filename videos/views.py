from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'featured']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'views', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        return VideoSerializer
    
    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        video.views += 1
        video.save()
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['GET'])
    def featured(self, request):
        featured_videos = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_videos, many=True)
        return Response(serializer.data)
    
class VideoCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer
    permission_classes = [permissions.IsAuthenticated]