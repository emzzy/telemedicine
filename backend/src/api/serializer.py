from rest_framework import serializers
from users.models import UserAccount
from doctor.models import MedicalProfessional
from patient.models import Patient
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed


class PatientSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    class Meta:
        model = Patient
        fields = [
            'user', 'full_name', 'image', 'age', 'emergency_contact', 'medical_information', 'blood_group'
        ]


class DoctorProfileSerializer(serializers.Serializer):
    from shared.serializers import MedicalProfessionalsSerializer
    medicalprofessional = MedicalProfessionalsSerializer(read_only=True)
    
    # class Meta:
    #     model = UserAccount
    #     fields = [
    #         'id', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'gender', 'date_of_birth', 'location',
    #         'is_verified', 'medicalprofessional'
    #     ]


class ListDoctorsSerializer(serializers.ModelSerializer):
    #title = serializers.ImageField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    location = serializers.CharField(source='user.location')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    #image = serializers.ImageField()
    available_appointment_date = serializers.DateTimeField()
    
    class Meta:
        model = MedicalProfessional
        fields = [
            'id', 'title', 'first_name', 'last_name', 'email', 'location', 'phone_number', 'image', 'available_appointment_date'
        ]


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

    def validate_email(self, value):
        return value.lower()


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


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    """this class handles user password reset"""
    email = serializers.EmailField(min_length=2)

    #redirect_url = serializers.CharField(max_length = 500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    """Validate and process request for password reset"""
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    # class Meta:
    #     fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = UserAccount.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            user.set_password(password)
            user.save()
            
            return {'user': user}
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class GetCurrentUserSerializer(serializers.ModelSerializer):
    from shared.serializers import MedicalProfessionalsSerializer, PatientModelSerializer
    patient_profile = PatientModelSerializer(read_only=True)
    medicalprofessional = MedicalProfessionalsSerializer(read_only=True)

    class Meta:
        model = UserAccount
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'location', 'date_joined', 'is_active', 'is_admin',
            'is_staff', 'is_superuser', 'is_verified', 'is_patient', 'is_medical_professional', 'patient_profile', 'medicalprofessional'
        ]