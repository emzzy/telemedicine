from rest_framework import serializers
from .models import Patient, MedicalProfessional, UserAccount

class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = [
        ]
        extra_kwargs = {"medical_information": {"required": False}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'passwords do not match'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = UserAccount.objects.create_user(
            email=validated_data.pop('email'),
            password=password,
            first_name=validated_data.pop('first_name'),
            last_name=validated_data.pop('last_name')
        )
        user.is_patient = True
        user.save()
        # create patient data
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class MedicalProfessionalSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = MedicalProfessional
        fields = [
            "title",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
            "gender",
            "medical_license",
            "years_of_experience",
            "date_of_birth",
            "is_active"
        ]

    def validate(self, data):
        user_data = data.get("user", {})
        if user_data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('passwords do not match')
        return data
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        
        # user = UserAccount.objects.create_user(
        #     email=validated_data.pop('email'),
        #     password=password,
        #     first_name=validated_data.pop('first_name'),
        #     last_name=validated_data.pop('last_name')
        # )
        user = UserAccount.objects.create_user(**user_data, password=password)
        user.is_medical_professional = True
        user.save()

        medical_professional = MedicalProfessional.objects.create(user=user, **validated_data)
        return medical_professional