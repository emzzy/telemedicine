from rest_framework import serializers
from .models import MedicalProfessional

class MedicalProfessionalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = [
            'title', 
            'image', 
            'bio', 
            'medical_license', 
            'specialty', 
            'years_of_experience',
            'professional_certificate', 
            'available_appointment_date'
        ]