from rest_framework import serializers
from .models import Patient, MedicalProfessional, Appointments

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "username",
            "last_name",
            "password",
            "email",
            "phone_number",
            "gender",
            "location",
            "date_of_birth",
            "age"
        ]


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = [
            "title",
            "username",
            "last_name",
            "password",
            "email",
            "phone_number",
            "gender",
            "specialty",
            "years_of_experience",
            "date_registered",
            "is_active"
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = [
            "id",
            "patient",
            "medical_professional",
            "date_time",
            "duration_minutes",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]