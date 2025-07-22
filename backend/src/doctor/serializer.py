from rest_framework import serializers
from doctor.models import Notification
from base.models import Appointment, LabTest, MedicalRecord, Billing
from shared.serializers import MedicalProfessionalsSerializer
from base.serializers import BookAppointmentSerializer, MedicalRecordSerializer, LabTestSerializer, PresicriptionSerilizer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'seen', 'date', 'appointment_id']


class DashboardSerializer(serializers.Serializer):
    doctor = MedicalProfessionalsSerializer()
    appointments = BookAppointmentSerializer(many=True)
    notifications = NotificationSerializer(many=True)

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointment_date', 'issues', 'symptoms', 'appointment_id']


class ViewAppointmentSerializer(serializers.Serializer):
    appointment = BookAppointmentSerializer()
    medical_records = MedicalRecordSerializer(many=True)
    lab_tests = LabTestSerializer(many=True)
    prescription = PresicriptionSerilizer(many=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ['__all__']


class DoctorProfileSerializer(serializers.ModelSerializer):
    medicalprofessional = MedicalProfessionalsSerializer()
    
    class Meta:
        from users.models import UserAccount
        
        model = UserAccount
        fields = [
            'id', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'gender', 'date_of_birth', 'location',
            'is_verified', 'medicalprofessional'
        ]
    
    def update(self, instance, validated_data):
        from .models import MedicalProfessional

        medicalprofessional_data = validated_data.pop('medicalprofessional', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        MedicalProfessional.objects.update_or_create(
            user=instance,
            defaults=medicalprofessional_data
        )
        return instance


class UpdateDoctorProfileSerializer(serializers.ModelSerializer):    
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    gender = serializers.CharField(source='user.gender')
    date_of_birth = serializers.CharField(source='user.date_of_birth')
    location = serializers.CharField(source='user.location')

    class Meta:
        from doctor.models import MedicalProfessional

        model = MedicalProfessional
        fields = [
            'title', 'bio', 'specialty', 'years_of_experience', 'medical_license', 'available_appointment_date', 'image',
            'professional_certificate', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'location'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance
