from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, UserViewSet, GameViewSet, GuideViewSet

# API router for DRF
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
router.register(r'guides', GuideViewSet)

urlpatterns = [
    path('', home, name='home'),  # Homepage route
    path('api/', include(router.urls)),  # API routes (e.g., /api/users/, /api/games/)
]
