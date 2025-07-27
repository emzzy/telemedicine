from django.urls import path
from .views import (
    patient_dashboard, appointment_detail, payments, notification, mark_notification_as_seen, patient_profile_data, 
    update_profile_data, cancel_appointment, complete_appointment
)

urlpatterns = [
    path('dashboard/', patient_dashboard, name='patient-dashboard'),
    path('appointment/<appointment_id>/detail/', appointment_detail, name='appointment-detail'),
    path('appointment/<appointment_id>/cancel/', cancel_appointment, name='cancel-appointment'),
    path('appointment/<appointment_id>/complete/', complete_appointment, name='complete-appointment'),
    path('payments/', payments, name='payments'),
    path('notifications/', notification, name='notifications'),
    path('notification/<id>/seen/', mark_notification_as_seen, name='mark-notification-as-seen'),
    path('profile/', patient_profile_data, name='patient-profile-data'),
    path('update-profile/', update_profile_data, name='update-profile-data'),
]