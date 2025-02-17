from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GameViewSet, GuideViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)  # This registers the /users/ endpoint
router.register(r'games', GameViewSet)
router.register(r'guides', GuideViewSet)

urlpatterns = [
    path('', include(router.urls)),  # This includes all registered viewsets in the router
]
