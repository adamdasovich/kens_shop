import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import PaymentIntent, PaymentMethod
from orders.models import Order
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()
logger = logging.getLogger(__name__)

class StripeService:
    @staticmethod
    def create_customer(user):
        """Create a Stripe customer for a user"""
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}",
                metadata={
                    'user_id': user.id,
                    'username': user.username
                }
            )
            return customer
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe customer: {e}")
            raise

    @staticmethod
    def get_or_create_customer(user):
        """Get existing customer or create new one"""
        try:
            # Try to find existing customer by email
            customers = stripe.Customer.list(email=user.email, limit=1)
            
            if customers.data:
                return customers.data[0]
            else:
                return StripeService.create_customer(user)
        except stripe.error.StripeError as e:
            logger.error(f"Error getting/creating Stripe customer: {e}")
            raise

    @staticmethod
    def create_payment_intent(user, amount, currency='usd', order=None, metadata=None):
        """Create a Stripe Payment Intent"""
        try:
            # Get or create Stripe customer
            customer = StripeService.get_or_create_customer(user)
            
            # Prepare metadata
            intent_metadata = {
                'user_id': user.id,
                'user_email': user.email,
            }
            if order:
                intent_metadata.update({
                    'order_id': order.id,
                    'order_number': order.order_number,
                })
            if metadata:
                intent_metadata.update(metadata)
            
            # Create Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                customer=customer.id,
                metadata=intent_metadata,
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            # Save to database
            payment_intent = PaymentIntent.objects.create(
                user=user,
                order=order,
                stripe_payment_intent_id=intent.id,
                client_secret=intent.client_secret,
                amount=amount,
                currency=currency,
                status=intent.status,
                metadata=intent_metadata
            )
            
            return payment_intent, intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating payment intent: {e}")
            raise

    @staticmethod
    def update_payment_intent_status(payment_intent_id, status, payment_method_id=None):
        """Update payment intent status"""
        try:
            payment_intent = PaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id
            )
            payment_intent.status = status
            if payment_method_id:
                payment_intent.payment_method_id = payment_method_id
            payment_intent.save()
            
            # Update order status based on payment status
            if payment_intent.order:
                if status == 'succeeded':
                    payment_intent.order.status = 'confirmed'
                    payment_intent.order.save()
                elif status == 'failed':
                    payment_intent.order.status = 'cancelled'
                    payment_intent.order.save()
            
            return payment_intent
            
        except PaymentIntent.DoesNotExist:
            logger.error(f"PaymentIntent not found: {payment_intent_id}")
            raise

    @staticmethod
    def save_payment_method(user, payment_method_id):
        """Save a payment method for future use"""
        try:
            # Get payment method from Stripe
            pm = stripe.PaymentMethod.retrieve(payment_method_id)
            
            # Save to database
            payment_method, created = PaymentMethod.objects.get_or_create(
                user=user,
                stripe_payment_method_id=payment_method_id,
                defaults={
                    'card_brand': pm.card.brand if pm.card else '',
                    'card_last4': pm.card.last4 if pm.card else '',
                    'card_exp_month': pm.card.exp_month if pm.card else None,
                    'card_exp_year': pm.card.exp_year if pm.card else None,
                }
            )
            
            return payment_method
            
        except stripe.error.StripeError as e:
            logger.error(f"Error saving payment method: {e}")
            raise

    @staticmethod
    def calculate_total_with_tax(amount, tax_rate=0.08):
        """Calculate total amount including tax"""
        tax_amount = amount * tax_rate
        total_amount = amount + tax_amount
        return {
            'subtotal': amount,
            'tax_amount': tax_amount,
            'total': total_amount
        }
