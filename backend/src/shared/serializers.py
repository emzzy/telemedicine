from rest_framework import serializers
from doctor.models import MedicalProfessional
from users.models import UserAccount
from patient.models import Patient


class UserAccountSerializer(serializers.ModelSerializer):
    #patient = PatientSerializer(read_only=True)
    #medical_professional = MedicalProfessionalSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = (
            'id', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'gender', 'date_of_birth', 'location',
            'is_patient', 'is_medical_professional'
        )


class MedicalProfessionalsSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = MedicalProfessional
        fields = [
            'id', 'user', 'title', 'image', 'bio', 'medical_license', 'specialty', 'years_of_experience',
            'professional_certificate', 'available_appointment_date'
    ]
        

class PatientModelSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    
    class Meta:
        model = Patient
        fields = [
            'user', 'full_name', 'image', 'age', 'emergency_contact', 'medical_information', 'blood_group'
        ]