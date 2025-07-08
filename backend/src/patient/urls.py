from django.urls import path
from .views import patient_dashboard, appointment_detail

urlpatterns = [
    path('dashboard/', patient_dashboard, name='patient-dashboard'),
    path('appointments/<appointment_id>/', appointment_detail, name='appointment-details'),
]
