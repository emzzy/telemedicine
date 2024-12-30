from rest_framework import serializers
from .models import Patient, MedicalProfessional

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__' # ["first_name", "last_name"]


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = '__all__'