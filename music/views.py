from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.http import JsonResponse
from .models import Track, Artist, Album, Genre, Like, Dislike, UserGenreScore, User


def track_list(request):
    tracks = Track.objects.select_related('artist', 'album').prefetch_related('genre').all()
    return render(request, 'music/track_list.html', {'tracks': tracks})


def track_detail(request, pk):
    track = get_object_or_404(
        Track.objects.select_related('artist', 'album').prefetch_related('genre'),
        pk=pk
    )
    return render(request, 'music/track_detail.html', {'track': track})


def random_track(request):
    track = Track.objects.exclude(audio_file='').order_by('?').first()
    if track:
        return redirect('track_detail', pk=track.pk)
    return redirect('track_list')


def artist_list(request):
    """Список исполнителей"""
    artists = Artist.objects.annotate(track_count=Count('tracks'))
    return render(request, 'music/artist_list.html', {'artists': artists})


def artist_detail(request, pk):
    """Страница исполнителя с его треками"""
    artist = get_object_or_404(Artist, pk=pk)
    tracks = artist.tracks.select_related('album', 'genre').all()
    return render(request, 'music/artist_detail.html', {
        'artist': artist,
        'tracks': tracks
    })
    
def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    tracks = album.tracks.all()
    return render(request, 'music/album_detail.html', {'album': album, 'tracks': tracks})


def track_like(request, track_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'}, status=401)
    
    track = get_object_or_404(Track, pk=track_id)
    
    existing_like = Like.objects.filter(user=request.user, track=track)
    
    if existing_like.exists():
        existing_like.delete()
        # уменьшить score для жанров
        return JsonResponse({'status': 'unliked'})
    else:
        Dislike.objects.filter(user=request.user, track=track).delete()
        Like.objects.create(user=request.user, track=track)
        # увеличить score для жанров
        return JsonResponse({'status': 'liked'})
    
def track_dislike(request, track_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login reqired'}, status=401)
    
    track = get_object_or_404(Track, pk=track_id)
    
    existing_dislike = Dislike.objects.filter(user=request.user, track=track)
    
    if existing_dislike.exists():
        existing_dislike.delete()
        for genre in track.genre.all():
            user_score, created = UserGenreScore.objects.get_or_create(user=request.user, genre=genre)
            user_score.score += 1
            user_score.save()
        return JsonResponse({'status': 'undisliked'})
    else:
        Like.objects.filter(user=request.user, track=track).delete()
        Dislike.objects.create(user=request.user, track=track)
        for genre in track.genre.all():
            user_score, created = UserGenreScore.objects.get_or_create(user=request.user, genre=genre)
            user_score.score -= 1
            user_score.save()
        return JsonResponse({'status': 'disliked'})

def random_track_api(request):
    tracks = Track.objects.filter(audio_file__isnull=False)
    if request.user.is_authenticated:
        tracks = tracks.exclude(dislike__user=request.user)
    track = tracks.order_by('?').first()
    if track:
        return JsonResponse({
            'id': track.pk,
            'title': track.title,
            'artist': track.artist.name,
            'audio_url': track.audio_file.url,
            'cover_url': track.cover.url if track.cover else None,
            'duration': track.duration,
        })
    return JsonResponse({'status': 'empty', 'message': 'No tracks available'})

def random_chat(request):
    users = User.objects.exclude(id=request.user.id).order_by('?')
    if users.exists():
        return redirect('profile', username=users.first().username)
    return redirect('track_list')

def chat_list(request):
    return render(request, 'music/chat_list.html')