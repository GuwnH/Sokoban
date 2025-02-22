from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Game, Guide, User
from .serializers import GameSerializer, GuideSerializer, UserSerializer
from .forms import GuideForm

# New homepage view (renders HTML)
def home(request):
    return render(request, 'home.html',{})  # Assumes "home.html" exists in your templates folder

def signin(request):
    return render(request, 'sign-in.html',{})  # Assumes "home.html" exists in your templates folder

def signup(request):
    return render(request, 'sign-up.html',{})  # Assumes "home.html" exists in your templates folder

def create_guide(request):
    if request.method == 'POST':
        form = GuideForm(request.POST)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.user = request.user  # Assign the logged-in user
            guide.save()
            return redirect('home')  # Redirect after successful creation
    else:
        form = GuideForm()
    
    return render(request, 'make_guides.html', {'form': form})

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
