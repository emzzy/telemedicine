from django.urls import path
from . import views
from .views import PatientSignupView, SelectedRole, list_users, IsPatientView, IsMedicalProfessional
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('patient-register/', PatientSignupView.as_view(), name='patient-register'),
    path('signup-patient/', views.user_signup, name='signup-patient'),
    #
    path('select-role/', SelectedRole.as_view(), name='select-role'),
    path('all-users/', views.list_users, name='all-users'), # returns all users from table
    path('get-user/<int:pk>', views.get_user, name='get-user'), # returns one user with their pk
    path('is-patient/', IsPatientView.as_view(), name='is-patient'), # returns only patients from table
    path('is-medical-professional/', IsMedicalProfessional.as_view(), name='is-medical-professional'), # returns only med prof from table
]
urlpatterns = format_suffix_patterns(urlpatterns)