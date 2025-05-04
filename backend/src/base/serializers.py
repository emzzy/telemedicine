from rest_framework import serializers
from .models import Service, Appointment, MedicalRecord, LabTest, Prescription, Billing


class ServicesListSerializer(serializers.ModelSerializer):
    from api.serializer import UserAccountSerializer
    doctor_count = serializers.SerializerMethodField()
    available_doctors = UserAccountSerializer(many=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'cost', 'doctor_count', 'image', 'available_doctors']

    def get_doctor_count(self, obj):
        return obj.available_doctors.count()
    

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
    
