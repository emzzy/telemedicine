from django.urls import path
from .views import get_user, create_user, get_all_users, user_details

urlpatterns = [
    path('user/', get_user, name='get_user'), # one user
    path('users/', get_all_users, name='get_all_users'), # all users
    path('user/create/', create_user, name='create_user'),
    path('users/<int:pk>', user_details, name='user_details')
]