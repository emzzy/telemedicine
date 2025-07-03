from django.urls import path
from .views import (
    dashboard, appointment_detail, cancel_appointment, complete_appointment, add_medical_record, add_lab_test, payments, notifications,
    mark_notification_as_seen, doctor_profile
)


urlpatterns = [
    path('dashboard/', dashboard, name='user-dashboard'),
    path('appointment/<int:appointment_id>/', appointment_detail, name='view-appointment'),
    path('appointment/<int:appointment_id>/cancel/', cancel_appointment, name='view-appointment'),
    path('appointment/<int:appointment_id>/complete/', complete_appointment, name='view-appointment'),
    path('appointment/<int:appointment_id>/add-record/', add_medical_record, name='add-medical-report'),
    path('appointment/<int:appointment_id>/<int:report_id>/edit/', add_medical_record, name='add-medical-report'),
    path('appointment/<int:appointment_id>/add-lab-test/', add_lab_test, name='lab-test'),
    path('appointment/<int:appointment_id>/lab_tests/<int:test_id>/edit/', add_lab_test, name='edit-lab-test'),
    path('appointment/<int:appointment_id>/add/', add_lab_test, name='add-prescription'),
    path('appointment/<int:appointment_id>/edit/', add_lab_test, name='edit-prescription'),
    path('payments/', payments, name='payments'),
    path('notifications/', notifications, name='payments'),
    path('notifications/<int:id>/seen/', mark_notification_as_seen, name='mark-notification-seen'),
    path('profile/', doctor_profile, name='doctor-profile')
]