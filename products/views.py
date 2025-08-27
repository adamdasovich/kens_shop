from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
        

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'featured']
    search_fields = ['name', 'description', 'materials']
    ordering_fields = ['created_at', 'price', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    def get_permissions(self):
        """
        Showcase (list and retrieve) is available to all users.
        Store functionality (create, update, delete) requires authentication
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['GET'])
    def featured(self, request):
        #get featured products
        featured_products = self.queryset.filter(featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def available(self, request):
        available_products = self.queryset.filter(status='available')
        serializer = self.get_serializer(available_products, many=True)
        return Response(serializer.data)
    
