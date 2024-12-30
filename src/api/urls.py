from django.urls import path
from .views import get_user, create_user, get_all_users

urlpatterns = [
    path('user/', get_user, name='get_user'),
    path('users/', get_all_users, name='get_all_users'),
    path('users/create/', create_user, name='create_user')
]