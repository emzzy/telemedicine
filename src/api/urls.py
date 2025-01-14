from django.urls import path
from . import views
from .views import PatientSignupView, SelectedRole
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #path('patients/', views.PatientListAPIView.as_view(), name='patients-list'), # all patients
    # path('patients/<int:pk>', views.PatientDetailsAPIView.as_view(), name='patient-details'),
    # path('doctors/', views.MedicalProfessionalListAPIView.as_view(), name='doctors-list'),
    # path('doctors/<int:pk>', views.MedicalProfessionalDetailsAPIView.as_view(), name='doctor-details'),
    path('patient-register/', PatientSignupView.as_view(), name='patient-register'),
    path('signup-patient/', views.signup_patient, name='signup-patient'),
    path('select-role/', SelectedRole.as_view(), name='select-role')
]
urlpatterns = format_suffix_patterns(urlpatterns)