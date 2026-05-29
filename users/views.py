from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Profile, Friend, Message
from music.models import SeenUser
from music.models import UserGenreScore, UserArtistScore
from django.db import models
from django.http import JsonResponse

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

@login_required
def chat_list(request):
    # Найти всех, с кем переписывался пользователь
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    chat_user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=chat_user_ids)
    
    # Для каждого — последнее сообщение
    chats = []
    for user in chat_users:
        last_msg = Message.objects.filter(
            (models.Q(sender=request.user, receiver=user) | models.Q(sender=user, receiver=request.user))
        ).order_by('-created_at').first()
        chats.append({'user': user, 'last_msg': last_msg})
    
    # Сортировать по дате последнего сообщения
    chats.sort(key=lambda x: x['last_msg'].created_at if x['last_msg'] else user.date_joined, reverse=True)
    
    return render(request, 'users/chat_list.html', {'chats': chats})

@login_required
def chat_view(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=receiver) |
        models.Q(sender=receiver, receiver=request.user)
    ).order_by('created_at')
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(sender=request.user, receiver=receiver, text=text)
        return redirect('chat_view', username=username)
    
    return render(request, 'users/chat.html', {
        'receiver': receiver,
        'messages': messages
    })
    

def search_users(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)
    
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[:10]
    
    results = []
    for u in users:
        avatar = None
        if hasattr(u, 'profile') and u.profile.avatar:
            avatar = u.profile.avatar.url
        results.append({
            'id': u.pk,
            'username': u.username,
            'avatar': avatar,
        })
    return JsonResponse(results, safe=False)

@login_required
def my_score(request):
    genre_scores = UserGenreScore.objects.filter(user=request.user).exclude(score=0).order_by('-score')
    artist_scores = UserArtistScore.objects.filter(user=request.user).exclude(score=0).order_by('-score')
    return render (request, 'users/my_score.html', {
        'genre_scores': genre_scores,
        'artist_scores': artist_scores
    })
    
@login_required
def users_history(request):
    seen_users = SeenUser.objects.filter(user=request.user).select_related('seen__profile').order_by('-created_at')
    return render(request, 'users/users_history.html', {'seen_users': seen_users})