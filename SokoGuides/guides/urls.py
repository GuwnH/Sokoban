from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, signin, signup, create_guide, guide_detail, profile_detail, search_guides, UserViewSet, GameViewSet, GuideViewSet

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
    path('guides/<int:guide_id>/', guide_detail, name='guide_detail'),
    path('profiles/<int:user_id>/', profile_detail, name='profile_detail'),
    path('search/', search_guides, name='search_guides'),
]
