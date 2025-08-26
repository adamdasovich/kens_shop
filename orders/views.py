from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        # generate unique order number
        order_number = get_random_string(8).upper()
        while Order.objects.filter(order_number=order_number).exists():
            order_number = get_random_string(8).upper()
        serializer.save(user=self.request.user, order_number=order_number)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        #Cancel an order
        order = self.get_object()
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            return Response({'message': 'Order cancelled successfully'})
        return Response(
            {'error': 'Cannot cancel order in current status'},
            status=status.HTTP_400_BAD_REQUEST
        )