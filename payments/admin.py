from django.contrib import admin
from .models import PaymentIntent, PaymentMethod

@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = ('stripe_payment_intent_id', 'user', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('stripe_payment_intent_id', 'user__username', 'user__email')
    readonly_fields = ('stripe_payment_intent_id', 'client_secret', 'created_at', 'updated_at')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_brand', 'card_last4', 'is_default', 'created_at')
    list_filter = ('card_brand', 'is_default', 'created_at')
    search_fields = ('user__username', 'user__email', 'card_last4')
