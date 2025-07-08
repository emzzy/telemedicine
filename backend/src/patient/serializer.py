from rest_framework import serializers
from .models import Patient, Notification
from base import models as base_models
from base import serializers as base_serializers
from shared.serializers import PatientModelSerializer
from base import serializers as base_serializers

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'patient', 'appointment', 'type', 'seen', 'date'
        ]


class PatientAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = base_models.Appointment
        fields = [
            'service', 'doctor', 'patient', 'appointment_date', 'issues', 'symptoms', 'appointment_id', 'status'
        ]


class PatientDashboardSerializer(serializers.Serializer):
    patient = PatientModelSerializer()
    appointments = PatientAppointmentSerializer(many=True)
    notifications = NotificationSerializer(many=True)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)