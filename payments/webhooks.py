import json
import stripe
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .services import StripeService
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        logger.error("Invalid payload in Stripe webhook")
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in Stripe webhook")
        return HttpResponseBadRequest("Invalid signature")

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        StripeService.update_payment_intent_status(
            payment_intent['id'], 
            'succeeded',
            payment_intent.get('payment_method')
        )
        logger.info(f"Payment succeeded: {payment_intent['id']}")
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        StripeService.update_payment_intent_status(
            payment_intent['id'], 
            'failed'
        )
        logger.info(f"Payment failed: {payment_intent['id']}")
        
    elif event['type'] == 'payment_intent.canceled':
        payment_intent = event['data']['object']
        StripeService.update_payment_intent_status(
            payment_intent['id'], 
            'canceled'
        )
        logger.info(f"Payment canceled: {payment_intent['id']}")
    
    else:
        logger.info(f"Unhandled event type: {event['type']}")

    return HttpResponse(status=200)
