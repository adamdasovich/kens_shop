from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order
import uuid

User = get_user_model()

class PaymentIntent(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
        ('requires_action', 'Requires Action'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_intents')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_intent', null=True, blank=True)
    
    # Stripe fields
    stripe_payment_intent_id = models.CharField(max_length=200, unique=True)
    client_secret = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Payment method details
    payment_method_id = models.CharField(max_length=200, blank=True)
    payment_method_type = models.CharField(max_length=50, blank=True)  # card, etc.
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"PaymentIntent {self.stripe_payment_intent_id} - ${self.amount}"

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    stripe_payment_method_id = models.CharField(max_length=200, unique=True)
    
    # Card details (if card payment method)
    card_brand = models.CharField(max_length=20, blank=True)  # visa, mastercard, etc.
    card_last4 = models.CharField(max_length=4, blank=True)
    card_exp_month = models.IntegerField(null=True, blank=True)
    card_exp_year = models.IntegerField(null=True, blank=True)
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.card_last4:
            return f"{self.card_brand.title()} ending in {self.card_last4}"
        return f"Payment Method {self.stripe_payment_method_id}"
