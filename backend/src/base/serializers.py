from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = []


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
    
