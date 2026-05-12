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
]