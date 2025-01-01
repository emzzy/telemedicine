from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('patients/', views.PatientListAPIView.as_view(), name='patients-list'), # all patients
    path('patients/<int:pk>', views.PatientDetailsAPIView.as_view(), name='patient-details'),
    path('doctors/', views.MedicalProfessionalListAPIView.as_view(), name='doctors-list'),
    path('doctors/<int:pk>', views.MedicalProfessionalDetailsAPIView.as_view(), name='doctor-details'),
]
urlpatterns = format_suffix_patterns(urlpatterns)