from base import models as base_models
from doctor.models import MedicalProfessional, Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import DashboardSerializer, NotificationSerializer
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    try:
        #doctor = MedicalProfessional.user.objects.get(user=request.user)
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointments = base_models.Appointment.objects.filter(doctor=doctor).select_related('patient__user')
    notification = Notification.objects.filter(doctor=doctor)
    
    data = {
        'doctor': doctor,
        'appointments': appointments,
        'notifications': notification
    }
    serializer = DashboardSerializer(data)
    
    return Response(serializer.data)