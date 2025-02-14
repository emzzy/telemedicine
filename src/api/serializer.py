from rest_framework import serializers
from users.models import UserAccount
from profiles.models import Patient, MedicalProfessional
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = [
            'location', 'age', 'emergency_contact', 'medical_information', 'user_type'
        ]

class MedicalProfessionalSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MedicalProfessional
        fields = [
            'title', 'medical_license', 'specialty', 'years_of_experience', 'user_type'
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    medical_professional = MedicalProfessionalSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = (
            'id', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'gender', 'date_of_birth', 'location',
            'is_patient', 'is_medical_professional', 'patient', 'medical_professional'
        )

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role = serializers.ChoiceField(choices=['patient', 'medical_professional'], required=True)

    class Meta:
        model = UserAccount
        fields = (
            'id', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'phone_number', 'gender',
            'date_of_birth', 'location', 'is_patient', 'is_medical_professional', 'role'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, attrs):
        # check if password and confirm password data match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # check if user is not both patient and medical professional
        if attrs.get('is_patient') and attrs.get('is_medical_professional'):
            raise serializers.ValidationError({'role': 'A user cannot be both patient and medical professional'})
        
        role = attrs.get('role')
        if role not in ['patient', 'medical_professional']:
            raise serializers.ValidationError({'role': 'invalid role selected.'})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = self.data.pop('role', None) # selected user role patient or medpro

        # create user with selected fields
        user = UserAccount.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            gender=validated_data.get('gender'),
            date_of_birth=validated_data.get('date_of_birth', None),
            location=validated_data.get('location', ''),
        )
        if role == 'patient':
            user.is_patient = True
        elif role == 'medical_professional':
            user.is_medical_professional = True
        
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = UserAccount
        fields = ['token']
        
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')