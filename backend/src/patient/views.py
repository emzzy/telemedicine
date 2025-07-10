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
from .serializer import PatientDashboardSerializer, AppointmentDetailSerializer, PatientProfileSerializer
from .permissions import IsPatient

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)
    total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(total_spent=models.Sum("total"))['total_spent'] or 0

    data = {
        'patient': patient,
        'appointments': appointments,
        'notifications': notifications,
        'total_spent': total_spent
    }
    serializer = PatientDashboardSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def appointment_detail(request, appointment_id):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, patient=patient)
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)
    
    serializer = AppointmentDetailSerializer ({
        'appointment': appointment,
        'medical_records': medical_records,
        'lab_tests': lab_tests,
        'prescription': prescriptions
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def cancel_appointment(request, appointment_id):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, patient=patient)
    if appointment.status in ['Completed', 'Cancelled']:
        return Response({'response': 'Appointment cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
    appointment.status = 'Cancelled'
    appointment.save()

    return Response({'response': 'Appointment cancelled successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def complete_appointment(request, appointment_id):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, patient=patient)
    if appointment.status in ['Completed', 'Cancelled']:
        return Response({'error': 'Appointment cannot be completed'}, status=status.HTTP_400_BAD_REQUEST)
    appointment.status = 'Completed'
    appointment.save()

    return Response({'response': 'Appointment completed successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def payments(request):
    from base import serializers as base_serializers
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    payments = base_models.Billing.objects.filter(appointment__patient=patient, status='Paid')
    serializer = base_serializers.BillingSerializer(payments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def notification(request):
    from patient.serializer import NotificationSerializer
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    notifications = Notification.objects.filter(patient=patient, seen=False)
    serializer = NotificationSerializer(notifications, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPatient])
def mark_notification_as_seen(request, id):
    try:
        patient = request.user.patient
        notification = Notification.objects.get(patient=patient, id=id)
        notification.seen = True
        notification.save()
    
        return Response({'meessage': 'Notification has been marked as seen'}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def patient_profile_data(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PatientProfileSerializer(instance={'patient': patient})

    return Response(serializer.data, status=status.HTTP_200_OK)


def edit_profile(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    formatted_next_available_appointment_date = patient.next_available_appointment_date.strftime()
