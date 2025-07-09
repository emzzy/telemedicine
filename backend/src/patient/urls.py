from django.urls import path
from .views import patient_dashboard, appointment_detail, payments, notification, mark_notification_as_seen

urlpatterns = [
    path('dashboard/', patient_dashboard, name='patient-dashboard'),
    path('appointment/<appointment_id>/detail/', appointment_detail, name='appointment-detail'),
    path('appointment/<appointment_id>/cancel/', appointment_detail, name='cancel-appointment'),
    path('appointment/<appointment_id>/complete/', appointment_detail, name='complete-appointment'),
    path('payments/', payments, name='payments'),
    path('notifications/', notification, name='notifications'),
    path('notification/<id>/seen/', mark_notification_as_seen, name='mark-notification-as-seen'),
]