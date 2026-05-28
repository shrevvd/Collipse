from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_list, name='track_list'),
    path('track/<int:pk>/', views.track_detail, name='track_detail'),
    path('random/', views.random_track, name='random_track'),
    path('artists/', views.artist_list, name='artist_list'),
    path('artist/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('album/<int:pk>/', views.album_detail, name='album_detail'),
    path('random-api/', views.random_track_api, name='random_track_api'),
    path('track/<int:track_id>/like/', views.track_like, name='track_like'),
    path('track/<int:track_id>/dislike/', views.track_dislike, name='track_dislike'),
    path('random-chat/', views.random_chat, name='random_chat'),
    path('find-match/', views.find_match, name='find_match'),
    path('search-tracks/', views.search_tracks, name='search_tracks'),
    path('liked-tracks-api/', views.liked_tracks_api, name='liked_tracks_api'),
    path('recommend-genre/', views.recommend_by_genre, name='recommend_genre'),
    path('recommend-artist/', views.recommend_by_artist, name='recommend_artist'),
    path('upload/', views.upload_track, name='upload_track'),
    path('api/artists/', views.api_artists, name='api_artists'),
    path('api/albums/', views.api_albums, name='api_albums'),
    path('queue-api/', views.queue_api, name='queue_api'),
]