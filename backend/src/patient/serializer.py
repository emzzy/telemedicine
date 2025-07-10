from rest_framework import serializers
from .models import Patient, Notification
from base import models as base_models
from base import serializers as base_serializers
from shared.serializers import PatientModelSerializer
from base import serializers as base_serializers


class NotificationSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = [
            'id', 'patient', 'appointment', 'type', 'seen', 'date'
        ]


class PatientAppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
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


class AppointmentDetailSerializer(serializers.Serializer):
    appointment = PatientAppointmentSerializer()
    medical_records = base_serializers.MedicalRecordSerializer(many=True)
    lab_tests = base_serializers.LabTestSerializer(many=True)
    prescription = base_serializers.PresicriptionSerilizer(many=True)


class PatientProfileSerializer(serializers.Serializer):
    patient = PatientModelSerializer()


class UpdatePatientProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    gender = serializers.CharField(source='user.gender')
    date_of_birth = serializers.CharField(source='user.date_of_birth')
    location = serializers.CharField(source='user.location')

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'location', 'full_name', 'image',
            'age', 'image', 'emergency_contact', 'medical_information', 'blood_group'
        ]