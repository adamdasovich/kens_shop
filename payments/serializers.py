from rest_framework import serializers
from .models import PaymentIntent, PaymentMethod

class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = [
            'id', 'stripe_payment_intent_id', 'client_secret', 
            'amount', 'currency', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'stripe_payment_intent_id', 'client_secret', 'created_at']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'stripe_payment_method_id', 'card_brand', 
            'card_last4', 'card_exp_month', 'card_exp_year', 
            'is_default', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class CreatePaymentIntentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    save_payment_method = serializers.BooleanField(default=False)
    
    def validate_order_id(self, value):
        from orders.models import Order
        try:
            order = Order.objects.get(id=value, user=self.context['request'].user)
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found or doesn't belong to user")

class ConfirmPaymentSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField()
    payment_method_id = serializers.CharField(required=False)
