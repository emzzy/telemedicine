from rest_framework import serializers
from .models import Patient, MedicalProfessional, BaseUser

class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "phone_number",
            "gender",
            "location",
            "date_of_birth",
            "age"
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('passwords do not match')
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = BaseUser.objects.create_user(**validated_data)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfessional
        fields = [
            "title",
            "username",
            "last_name",
            "password",
            "email",
            "phone_number",
            "gender",
            "specialty",
            "years_of_experience",
            "date_registered",
            "is_active"
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('passwords do not match')
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = BaseUser.objects.create_user(**validated_data)
        user.is_medical_professional = True
        user.save()
        medical_professional = MedicalProfessional.objects.create(user=user, **validated_data)
        return medical_professional