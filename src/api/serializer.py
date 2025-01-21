from rest_framework import serializers
from users.models import UserAccount
from profiles.models import Patient, MedicalProfessional


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = (
            'location', 'age', 'emergency_contact', 'medical_information', 'user_type'
        )
        extra_kwargs = {"medical_information": {"required": False}}


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MedicalProfessional
        fields = (
            'title', 'medical_license', 'specialty', 'years_of_experience'
        )


class UserAccountSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    medical_professional = MedicalProfessionalSerializer(read_only=True)
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = (
            'id', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'gender', 'date_of_birth', 'location',
            'is_patient', 'is_medical_professional'
        )