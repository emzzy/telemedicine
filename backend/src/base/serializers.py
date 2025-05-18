from rest_framework import serializers
from .models import Service, Appointment, MedicalRecord, LabTest, Prescription, Billing
from doctor.serializer import MedicalProfessionalsSerializer
from api.serializer import PatientSerializer, UserAccountSerializer, DoctorProfileSerializer


class ServicesListSerializer(serializers.ModelSerializer):
    doctor_count = serializers.SerializerMethodField()
    available_doctors = DoctorProfileSerializer(many=True)
    medicalprofessional = MedicalProfessionalsSerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'cost', 'doctor_count', 'image', 'available_doctors', 'medicalprofessional'
        ]

    def get_doctor_count(self, obj):
        return obj.available_doctors.count()
    

class BookAppointmentSerializer(serializers.ModelSerializer):
    issues = serializers.CharField(required=False, allow_blank=True)
    symptoms = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Appointment
        fields = [
            'service', 'doctor', 'patient', 'appointment_date', 'issues', 'symptoms'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord


class LabtestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
    
