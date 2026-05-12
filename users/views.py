from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Profile, Friend

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('track_list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('track_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('track_list')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    friends = Friend.objects.filter(user=user)
    
    if request.user.is_authenticated:
        is_friend = Friend.objects.filter(user=request.user, friend=user).exists()
    else:
        is_friend = False
    
    context = {
        'profile': profile,
        'friends': friends,
        'is_friend': is_friend,
        'likes_count': 0,
        'playlists_count': 0,
        'uploads_count': 0,
        'top_artists': [],
        'top_tracks': [],
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname', '')
        profile.bio = request.POST.get('bio', '')
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'users/edit_profile.html', {'profile': profile})

@login_required
def add_friend(request, username):
    friend_user = get_object_or_404(User, username=username)
    Friend.objects.get_or_create(user=request.user, friend=friend_user)
    return redirect('profile', username=username)

@login_required
def remove_friend(request, username):
    friend_user = get_object_or_404(User, username=username)
    Friend.objects.filter(user=request.user, friend=friend_user).delete()
    return redirect('profile', username=username)