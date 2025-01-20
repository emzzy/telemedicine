from django.urls import path
from . import views
from .views import PatientSignupView, SelectedRole, list_users
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('patient-register/', PatientSignupView.as_view(), name='patient-register'),
    path('signup-patient/', views.user_signup, name='signup-patient'),
    path('select-role/', SelectedRole.as_view(), name='select-role'),
    path('all-users/', views.list_users, name='all-users')
]
urlpatterns = format_suffix_patterns(urlpatterns)