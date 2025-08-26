from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from .models import Comment, Rating
from .serializers import *

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type', 'object_id']

    def get_queryset(self):
        return Comment.objects.filter(parent=None)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def for_product(self, request):
        # get comments for a specific product
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        product_type = ContentType.objects.get(model='product')
        comments = Comment.objects.filter(
            content_type=product_type,
            object_id=product_id,
            parent=None
        )
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    
class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['content_type', 'object_id', 'rating']

    def get_queryset(self):
        return Rating.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RatingCreateSerializer
        return RatingSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def for_product(self, request):
        #Get rating for a specific product
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        product_type = ContentType.objects.get(model='product')
        ratings = Rating.objects.filter(
            content_type=product_type,
            object_id=product_id
        )
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def average(self,request):
        # get average rating for a product
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        product_type = ContentType.objects.get(model='product')
        ratings = Rating.objects.filter(
            content_type=product_type,
            object_id=product_id
        )
        if ratings.exists():
            avg_rating = sum(r.rating for r in ratings) / len(ratings)
            return Response({
                'average_rating': round(avg_rating, 2),
                'total_ratings': len(ratings)
            })
        return Response({'average_rating': 0, 'total_ratings': 0})