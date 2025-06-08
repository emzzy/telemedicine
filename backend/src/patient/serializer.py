from rest_framework import serializers
from .models import Patient, Notification

class PatientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'full_name', 'image', 'verified', 'age', 'emergency_contact', 'medical_information', 'blood_group'
        ]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'patient', 'appointment', 'type', 'seen', 'date'
        ]