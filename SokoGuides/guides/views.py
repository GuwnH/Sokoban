from django.shortcuts import render
from rest_framework import viewsets
from .models import Game, Guide, User
from .serializers import GameSerializer, GuideSerializer, UserSerializer

# New homepage view (renders HTML)
def home(request):
    return render(request, 'home.html',{})  # Assumes "home.html" exists in your templates folder

# API Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
