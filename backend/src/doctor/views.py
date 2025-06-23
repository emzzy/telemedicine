from base import models as base_models
from doctor.models import MedicalProfessional, Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import DashboardSerializer, ViewAppointmentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from base.serializers import MedicalRecordSerializer, LabTestSerializer


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_detail(request, appointment_id):
    doctor = request.user.medicalprofessional
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    medical_records = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    serializer = ViewAppointmentSerializer ({
        'appointment': appointment,
        'medical_records': medical_records,
        'lab_tests': lab_tests,
        'prescription': prescriptions
    })
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_appointment(request, appointment_id):
    doctor = request.user.medicalprofessional
    appointment = get_object_or_404(
        base_models.Appointment,
        appointment_id=appointment_id,
        doctor=doctor
    )
    if appointment.status in ['Completed', 'Cancelled']:
        return Response({'response': 'Appointment cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
    appointment.status = 'Cancelled'
    appointment.save()

    return Response({'response': 'Appointment cancelled successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_appointment(request, appointment_id):
    doctor = request.user.medicalprofessional
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id,doctor=doctor)
    if appointment.status == 'Completed':
        return Response({'response': 'Appointment already completed.'}, status=status.HTTP_200_OK)
    appointment.status = 'Completed'
    appointment.save()

    return Response({'response': 'Appointment completed successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_medical_record(request, appointment_id):
    doctor = request.user.medicalprofessional
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)

    serializer = MedicalRecordSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(appointment=appointment)

        return Response({'Medical Report Added Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(IsAuthenticated)
def edit_medical_record(request, appointment_id, medical_report_id):
    doctor = request.user.medicalprofessional
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    medical_report = get_object_or_404(base_models.MedicalRecord, id=medical_report_id, appointment=appointment)
    
    if 'diagnosis' in request.data:
        medical_report.diagnosis = request.data['diagnosis']
    if 'treatment' in request.data:
        medical_report.treatment = request.data['treatment']
    medical_report.save()

    return Response({'data': 'Medical report updated successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lab_test(request, appointment_id):
    doctor = request.user.medicalprofessional
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    
    serializer = LabTestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(appointment=appointment)
        return Response({'message': 'Lab Test added successfully.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)