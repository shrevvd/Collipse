from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import Track, Artist, Album, Genre, Like, Dislike, UserGenreScore, User, UserArtistScore


def track_list(request):
    if request.user.is_authenticated and request.GET.get('tab') == 'likes':
        liked_ids = Like.objects.filter(user=request.user).values_list('track_id', flat=True)
        tracks = Track.objects.filter(id__in=liked_ids).select_related('artist', 'album').prefetch_related('genre')
    else:
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
        for genre in track.genre.all():
            user_score, _ = UserGenreScore.objects.get_or_create(user=request.user, genre=genre)
            user_score.score -= 2
            user_score.save()
        artist_score, _ = UserArtistScore.objects.get_or_create(user=request.user, artist=track.artist)
        artist_score.score -= 1
        artist_score.save()
        return JsonResponse({'status': 'unliked'})
    else:
        Dislike.objects.filter(user=request.user, track=track).delete()
        Like.objects.create(user=request.user, track=track)
        for genre in track.genre.all():
            user_score, _ = UserGenreScore.objects.get_or_create(user=request.user, genre=genre)
            user_score.score += 2
            user_score.save()
        artist_score, _ = UserArtistScore.objects.get_or_create(user=request.user, artist=track.artist)
        artist_score.score += 1
        artist_score.save()
        return JsonResponse({'status': 'liked'})
    
def track_dislike(request, track_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'}, status=401)
    
    track = get_object_or_404(Track, pk=track_id)
    existing_dislike = Dislike.objects.filter(user=request.user, track=track)
    
    if existing_dislike.exists():
        existing_dislike.delete()
        for genre in track.genre.all():
            user_score, _ = UserGenreScore.objects.get_or_create(user=request.user, genre=genre)
            user_score.score += 2
            user_score.save()
        artist_score, _ = UserArtistScore.objects.get_or_create(user=request.user, artist=track.artist)
        artist_score.score += 1
        artist_score.save()
        return JsonResponse({'status': 'undisliked'})
    else:
        Like.objects.filter(user=request.user, track=track).delete()
        Dislike.objects.create(user=request.user, track=track)
        for genre in track.genre.all():
            user_score, _ = UserGenreScore.objects.get_or_create(user=request.user, genre=genre)
            user_score.score -= 2
            user_score.save()
        artist_score, _ = UserArtistScore.objects.get_or_create(user=request.user, artist=track.artist)
        artist_score.score -= 1
        artist_score.save()
        return JsonResponse({'status': 'disliked'})

def random_track_api(request):
    track_id = request.GET.get('track_id')
    if track_id:
        track = get_object_or_404(Track, pk=track_id, audio_file__isnull=False)
    else:
        tracks = Track.objects.filter(audio_file__isnull=False)
        if request.user.is_authenticated:
            tracks = tracks.exclude(dislike__user=request.user)
        track = tracks.order_by('?').first()
    
    if track:
        is_liked = Like.objects.filter(user=request.user, track=track).exists() if request.user.is_authenticated else False
        is_disliked = Dislike.objects.filter(user=request.user, track=track).exists() if request.user.is_authenticated else False
        return JsonResponse({
            'id': track.pk,
            'title': track.title,
            'artist': track.artist.name,
            'audio_url': track.audio_file.url,
            'cover_url': track.cover.url if track.cover else None,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        })
    return JsonResponse({'status': 'empty', 'message': 'No tracks available'})

def random_chat(request):
    users = User.objects.exclude(id=request.user.id).order_by('?')
    if users.exists():
        return redirect('profile', username=users.first().username)
    return redirect('track_list')

def chat_list(request):
    return render(request, 'music/chat_list.html')

def search_tracks(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)
    
    tracks = Track.objects.filter(
        Q(title__icontains=query) | Q(artist__name__icontains=query)
    ).select_related('artist').exclude(audio_file='')[:10]
    
    results = []
    for t in tracks:
        results.append({
            'id': t.pk,
            'title': t.title,
            'artist': t.artist.name,
            'audio_url': t.audio_file.url if t.audio_file else None,
            'cover_url': t.cover.url if t.cover else None,
        })
    return JsonResponse(results, safe=False)

def liked_tracks_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'}, status=401)
    
    liked_track_ids = Like.objects.filter(user=request.user).values_list('track_id', flat=True)
    track = Track.objects.filter(id__in=liked_track_ids, audio_file__isnull=False).order_by('?').first()
    
    if track:
        is_liked = True
        is_disliked = Dislike.objects.filter(user=request.user, track=track).exists()
        return JsonResponse({
            'id': track.pk,
            'title': track.title,
            'artist': track.artist.name,
            'audio_url': track.audio_file.url,
            'cover_url': track.cover.url if track.cover else None,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        })
    return JsonResponse({'status': 'empty', 'message': 'No liked tracks'})
