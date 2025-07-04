from django.shortcuts import render, get_object_or_404
from django.db import models
from patient.models import Patient, Notification
from base import models as base_models
from patient import models as patient_models
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializer import PatientDashboardSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)
    total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(total_spent=models.Sum("total"))['total_spent']

    data = {
        'patient': patient,
        'appointments': appointments,
        'notifications': notifications,
        'total_spent': total_spent
    }
    serializer = PatientDashboardSerializer(data)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_detail(request, appointment_id):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, patient=patient)
    medical_records = get_object_or_404(base_models.MedicalRecord, appointment=appointment)
    lab_tests = get_object_or_404(base_models.LabTest, appointment=appointment)
    prescriptions = get_object_or_404(base_models.Prescription, appointment=appointment)

    
    