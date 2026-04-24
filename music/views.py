from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Track, Artist, Album, Genre


def track_list(request):
    tracks = Track.objects.select_related('artist', 'album', 'genre').all()
    return render(request, 'music/track_list.html', {'tracks': tracks})


def track_detail(request, pk):
    track = get_object_or_404(
        Track.objects.select_related('artist', 'album', 'genre'),
        pk=pk
    )
    return render(request, 'music/track_detail.html', {'track': track})


def random_track(request):
    """Рандомный трек — редирект на страницу трека"""
    track = Track.objects.order_by('?').first()
    return redirect('track_detail', pk=track.pk) if track else redirect('track_list')


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