from django.urls import path
from . import views


urlpatterns = [
    path('rooms/', views.RoomListCreateView.as_view(), name='room-list'),
    path('rooms/<slug:slug>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<slug:room_slug>/messages/', views.MessageListView.as_view(), name='room-messages'),
]