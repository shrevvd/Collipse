from django.contrib import admin
from .models import Genre, Artist, Album, Track, Like, Dislike, UserGenreScore

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
    list_display = ['title', 'artist', 'album', 'display_genre', 'uploaded_at']
    list_filter = ['artist', 'album']
    search_fields = ['title', 'artist__name']
    
    def display_genre(self, obj):
        return ", ".join([g.name for g in obj.genre.all()])
    display_genre.short_description = 'Жанры'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'track', 'created_at']
    search_fields = ['user__username', 'track__title']

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'track', 'created_at']
    search_fields = ['user__username', 'track__title']

@admin.register(UserGenreScore)
class UserGenreScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'genre', 'score']
    search_fields = ['user__username', 'genre__name']