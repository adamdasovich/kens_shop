from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
from .webhooks import stripe_webhook

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('stripe/webhook/', stripe_webhook, name='stripe_webhook'),
]