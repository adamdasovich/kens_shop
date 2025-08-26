from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'video-categories', VideoCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
