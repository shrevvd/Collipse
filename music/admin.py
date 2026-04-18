from django.contrib import admin
from .models import Genre, Artist, Album, Track

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date']
    list_filter = ['artist', 'release_date']
    search_fields = ['title', 'artist__name']

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'genre', 'uploaded_at']
    list_filter = ['artist', 'genre', 'album']
    search_fields = ['title', 'artist__name']