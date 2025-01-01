from rest_framework import serializers
from .models import Patient, MedicalProfessional

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__' # ["first_name", "last_name"]


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = [
            "title",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "specialty",
            "years_of_experience",
            "date_registered"
        ]