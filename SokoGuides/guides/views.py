from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Game, Guide, User, Image
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

def guide_detail(request, guide_id):
    # Fetch the guide by its ID
    guide = get_object_or_404(Guide, guide_id=guide_id)
    
    # Fetch related images for the guide
    images = Image.objects.filter(guide=guide)
    
    # Pass the guide and images to the template
    return render(request, 'view_guide.html', {
        'guide': guide,
        'images': images,
    })

def profile_detail(request, user_id):
    # Fetch the guide by its ID
    user = get_object_or_404(User, user_id=user_id)
    
    # Fetch related guides associated with the user
    guides = Guide.objects.filter(user=user_id)
    
    # Pass the guide and images to the template
    return render(request, 'profile.html', {
        'guides': guides,
        'user': user,
    })

def search_guides(request):
    # Get search parameters from the request
    game_name = request.GET.get('game_name', '')
    guide_level = request.GET.get('guide_level', '')
    user_name = request.GET.get('user_name', '')

    # Start with all guides
    guides = Guide.objects.all()

    # Filter by game name (case-insensitive)
    if game_name:
        guides = guides.filter(game__game_name__icontains=game_name)

    # Filter by guide level
    if guide_level:
        guides = guides.filter(guide_level=guide_level)

    # Filter by user name (case-insensitive)
    if user_name:
        guides = guides.filter(user__user_name__icontains=user_name)

    # Pass the filtered guides to the template
    return render(request, 'guide_search.html', {
        'guides': guides,
        'game_name': game_name,
        'guide_level': guide_level,
        'user_name': user_name,
    })

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
