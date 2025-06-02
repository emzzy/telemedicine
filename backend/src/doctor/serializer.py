from rest_framework import serializers
from doctor.models import Notification
from base.models import Appointment



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'seen', 'date', 'appointment']


class DashboardSerializer(serializers.Serializer):
    from shared.serializers import MedicalProfessionalsSerializer
    from base.serializers import BookAppointmentSerializer
    
    doctor = MedicalProfessionalsSerializer()
    appointments = BookAppointmentSerializer(many=True)
    notifications = NotificationSerializer(many=True)
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointment_date', 'issues', 'symptoms', 'appointment_id']

