from rest_framework import serializers
from .models import Patient, MedicalProfessional

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name"] #'__all__'


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = ["first_name", "last_name"] #'__all__'