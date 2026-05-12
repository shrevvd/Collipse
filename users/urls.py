from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('add-friend/<str:username>/', views.add_friend, name='add_friend'),
    path('remove-friend/<str:username>/', views.remove_friend, name='remove_friend'),
]