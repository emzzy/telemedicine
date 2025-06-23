from django.urls import path
from doctor.views import dashboard, appointment_detail, cancel_appointment, complete_appointment, add_medical_record, add_lab_test


urlpatterns = [
    path('dashboard/', dashboard, name='user-dashboard'),
    path('appointment/<int:appointment_id>/', appointment_detail, name='view-appointment'),
    path('appointment/<int:appointment_id>/cancel/', cancel_appointment, name='view-appointment'),
    path('appointment/<int:appointment_id>/complete/', complete_appointment, name='view-appointment'),
    path('appointment/<int:appointment_id>/add-record/', add_medical_record, name='add-medical-report'),
    path('appointment/<int:appointment_id>/<int:report_id/edit/', add_medical_record, name='add-medical-report'),
    path('appointment/<int:appointment_id>/add-lab-test/', add_lab_test, name='lab-test'),
]