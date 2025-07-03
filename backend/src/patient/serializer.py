from rest_framework import serializers
from .models import Patient, Notification
from base import models as base_models
from base import serializers as base_serializers
from shared.serializers import PatientModelSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'patient', 'appointment', 'type', 'seen', 'date'
        ]


class PatientDashboardSerializer(serializers.Serializer):
    patient = PatientModelSerializer()
    notifications = NotificationSerializer(many=True)
    
    class Meta:
        model = base_models.Appointment
        fields = [
            'service', 'doctor', 'appointments', 'issues', 'symptoms', 'appointment_date', 'total_spent', 'status'
        ]