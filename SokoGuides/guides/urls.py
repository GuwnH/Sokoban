from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, signin, signup, create_guide, UserViewSet, GameViewSet, GuideViewSet

# API router for DRF
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
router.register(r'guides', GuideViewSet)

urlpatterns = [
    path('', home, name='home'),  # Homepage route
    path('api/', include(router.urls)),  # API routes (e.g., /api/users/, /api/games/)
    path('sign-in', signin, name='sign-in'),
    path('sign-up', signup, name='sign-up'),
    path('guides/create/', create_guide, name='create_guide'),
]
