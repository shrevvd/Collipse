from django.contrib.auth import views as auth_views
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
    path('chat/<str:username>/', views.chat_view, name='chat_view'),
    path('chats/', views.chat_list, name='chat_list'),
    path('search-users/', views.search_users, name='search_users'),
    path('my-score/', views.my_score, name='my_score'),
    path('users-history/', views.users_history, name='users_history'),
    path('dislikes/', views.dislikes_list, name='dislikes'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
