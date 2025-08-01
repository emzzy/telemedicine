from rest_framework import serializers
from base.models import Service, Appointment, Billing, LabTest, Prescription, MedicalRecord
from shared.serializers import MedicalProfessionalsSerializer
from api.serializer import DoctorProfileSerializer
import datetime
from api.serializer import PatientSerializer


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
    patient = PatientSerializer()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'service', 'doctor', 'patient', 'appointment_date', 'issues', 'symptoms', 'status', 'appointment_id'
        ]


class BillingSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    class Meta:
        model = Billing
        fields = [
            'patient', 'appointment', 'sub_total', 'tax', 'total', 'status', 'billing_id', 'date'
        ]


class MedicalRecordSerializer(serializers.ModelSerializer):
    #appointment = BookAppointmentSerializer()
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment']


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['test_name', 'description', 'result']


class PresicriptionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['medication']

