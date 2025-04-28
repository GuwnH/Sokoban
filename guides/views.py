from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Game, Guide, UserProfile, Image
from .serializers import GameSerializer, GuideSerializer, UserSerializer, ImageSerializer
from .forms import GuideForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
import random
from django.conf import settings

def home(request):
    # Get today's date for consistent daily feature
    today = timezone.now().date()
    
    # Seed random with today's date for consistent daily selection
    random.seed(today.toordinal())
    
    try:
        # Get all approved guides
        approved_guides = Guide.objects.all()
        
        # Select a random featured guide for today
        featured_level = random.choice(approved_guides) if approved_guides.exists() else None
        
    except Exception as e:
        featured_level = None
    
    context = {
        'featured_level': featured_level,
        'today': today,
    }
    return render(request, 'home.html', context)

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'sign-in.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Check if username already exists
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Username already exists.")
            else:
                user = form.save()
                display_name = request.POST.get('user_display', user.username)
                UserProfile.objects.create(user=user, user_display=display_name)
                login(request, user)
                return redirect('home')
        else:
            # Django's form will auto-add errors for invalid fields
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'sign-up.html', {'form': form})

# Guide-related views
@login_required
def create_guide(request):
    games = Game.objects.all()  # Get all games from the database
    
    if request.method == "POST":
        # Create the guide
        guide = Guide.objects.create(
            game_id=request.POST['game'],
            guide_level=request.POST['guide_level'],
            title=request.POST['title'],
            guide_text=request.POST['guide_text'],
            number_of_moves=request.POST['number_of_moves'],
            colors_required=request.POST['colors_required'] == "True",
            user=request.user,  # Note: Changed from 'author' to 'user' to match your model
        )

        # Handle images
        images = request.FILES.getlist('images')
        alt_texts = request.POST.getlist('alt_texts')

        for img_file, alt_text in zip(images, alt_texts):
            Image.objects.create(
                guide=guide,
                image=img_file,  # Note: Your model has 'url' field but you're using file upload
                alt_text=alt_text
            )
        return redirect('guide_detail', guide_id=guide.guide_id)  # Redirect to the new guide
    
    return render(request, 'make_guides.html', {
        'games': games  # Pass the games queryset to the template
    })

def guide_detail(request, guide_id):
    guide = get_object_or_404(Guide, guide_id=guide_id)
    images = Image.objects.filter(guide=guide)
    return render(request, 'view_guide.html', {
        'guide': guide,
        'images': images,
        'MEDIA_URL': settings.MEDIA_URL,  # Ensure MEDIA_URL is passed into the context
    })

def profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, user_display=user.username)
    
    guides = Guide.objects.filter(user=user)
    return render(request, 'profile.html', {
        'guides': guides,
        'profile_user': user,
        'user_profile': profile,
    })

def search_guides(request):
    game_name = request.GET.get('game_name', '')
    guide_level = request.GET.get('guide_level', '')
    username = request.GET.get('username', '')

    guides = Guide.objects.all()

    if game_name:
        guides = guides.filter(game__game_name__icontains=game_name)
    if guide_level:
        guides = guides.filter(guide_level=guide_level)
    if username:
        guides = guides.filter(user__username__icontains=username)

    return render(request, 'guide_search.html', {
        'guides': guides,
        'game_name': game_name,
        'guide_level': guide_level,
        'username': username,
    })

def custom_logout(request):
    logout(request)
    return redirect('home')  # Or your preferred page

def about(request):
    return render(request, 'about.html')

def games(request):
    games = Game.objects.all()
    return render(request, 'games.html', {'games': games})

@login_required
def suggest_game(request):
    if request.method == 'POST':
        game_name = request.POST['game_name']
        number_levels = int(request.POST['number_levels'])
        additional_inputs = request.POST['additional_inputs'] == 'True'
        
        # Instead of saving directly, you could save to a separate "suggested games" model or notify an admin.
        Game.objects.create(
            game_name=game_name,
            number_levels=number_levels,
            weighted_ratings=0.00,
            additional_inputs=additional_inputs
        )
        return redirect('games')

# API Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminUser]

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]