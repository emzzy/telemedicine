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