from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import stripe
from .models import PaymentIntent, PaymentMethod
from .serializers import (
    PaymentIntentSerializer, 
    PaymentMethodSerializer,
    CreatePaymentIntentSerializer,
    ConfirmPaymentSerializer
)
from .services import StripeService
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        """Create a payment intent for an order"""
        serializer = CreatePaymentIntentSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(
                id=serializer.validated_data['order_id'],
                user=request.user
            )
            
            # Calculate total with tax
            totals = StripeService.calculate_total_with_tax(float(order.total_amount))
            
            payment_intent, stripe_intent = StripeService.create_payment_intent(
                user=request.user,
                amount=totals['total'],
                order=order,
                metadata={
                    'subtotal': str(totals['subtotal']),
                    'tax_amount': str(totals['tax_amount']),
                }
            )
            
            return Response({
                'client_secret': payment_intent.client_secret,
                'payment_intent_id': payment_intent.stripe_payment_intent_id,
                'amount': payment_intent.amount,
                'subtotal': totals['subtotal'],
                'tax_amount': totals['tax_amount'],
                'total': totals['total']
            })
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def confirm_payment(self, request):
        """Confirm a payment and update order status"""
        serializer = ConfirmPaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment_intent_id = serializer.validated_data['payment_intent_id']
            payment_method_id = serializer.validated_data.get('payment_method_id')
            
            # Retrieve the payment intent from Stripe
            stripe_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            # Update our database
            payment_intent = StripeService.update_payment_intent_status(
                payment_intent_id,
                stripe_intent.status,
                payment_method_id
            )
            
            # Save payment method if requested and successful
            if (payment_method_id and 
                stripe_intent.status == 'succeeded'):
                StripeService.save_payment_method(request.user, payment_method_id)
            
            return Response({
                'status': payment_intent.status,
                'order_id': payment_intent.order.id if payment_intent.order else None,
                'message': 'Payment confirmed successfully'
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def payment_methods(self, request):
        """Get user's saved payment methods"""
        payment_methods = PaymentMethod.objects.filter(user=request.user)
        serializer = PaymentMethodSerializer(payment_methods, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def delete_payment_method(self, request):
        """Delete a saved payment method"""
        payment_method_id = request.data.get('payment_method_id')
        
        try:
            payment_method = PaymentMethod.objects.get(
                stripe_payment_method_id=payment_method_id,
                user=request.user
            )
            
            # Detach from Stripe
            stripe.PaymentMethod.detach(payment_method_id)
            
            # Delete from database
            payment_method.delete()
            
            return Response({'message': 'Payment method deleted successfully'})
            
        except PaymentMethod.DoesNotExist:
            return Response(
                {'error': 'Payment method not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def config(self, request):
        """Get Stripe publishable key for frontend"""
        return Response({
            'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
