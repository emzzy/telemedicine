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