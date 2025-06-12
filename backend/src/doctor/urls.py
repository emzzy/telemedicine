from django.urls import path
from doctor.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='user-dashboard'),
]