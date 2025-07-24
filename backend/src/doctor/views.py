from base import models as base_models
from doctor.models import MedicalProfessional, Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import DashboardSerializer, ViewAppointmentSerializer, DoctorProfileSerializer, UpdateDoctorProfileSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from base.serializers import MedicalRecordSerializer, LabTestSerializer, PresicriptionSerilizer, BillingSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .permissions import IsDoctor

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def dashboard(request):
    try:
        #doctor = MedicalProfessional.user.objects.get(user=request.user)
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointments = base_models.Appointment.objects.filter(doctor=doctor).select_related('patient__user')
    notification = Notification.objects.filter(doctor=doctor, seen=False)
    
    data = {
        'doctor': doctor,
        'appointments': appointments,
        'notifications': notification
    }
    serializer = DashboardSerializer(data)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def appointment_detail(request, appointment_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

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
@permission_classes([IsAuthenticated, IsDoctor])
def cancel_appointment(request, appointment_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    if appointment.status in ['Completed', 'Cancelled']:
        return Response({'response': 'Appointment cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
    appointment.status = 'Cancelled'
    appointment.save()

    return Response({'response': 'Appointment cancelled successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def complete_appointment(request, appointment_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id,doctor=doctor)
    if appointment.status == 'Completed':
        return Response({'response': 'Appointment already completed.'}, status=status.HTTP_200_OK)
    appointment.status = 'Completed'
    appointment.save()

    return Response({'response': 'Appointment completed successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def add_medical_record(request, appointment_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)    
    
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    serializer = MedicalRecordSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(appointment=appointment)

        return Response({'Medical Report Added Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def edit_medical_record(request, appointment_id, medical_report_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

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
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    serializer = LabTestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(appointment=appointment)
        return Response({'message': 'Lab Test added successfully.'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def edit_lab_test(request, appointment_id, lab_test_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    lab_test = get_object_or_404(base_models.LabTest, id=lab_test_id, appointment=appointment)

    if 'test_name' in request.data:
        lab_test.test_name = request.data['test_name']
    if 'description' in request.data:
        lab_test.description = request.data['description']
    if 'result' in request.data:
        lab_test.result = request.data['result']
    lab_test.save()

    return Response({'message': 'Lab result saved successsfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def get_lab_tests(request, appointment_id, lab_test_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    lab_test = get_object_or_404(base_models.LabTest, id=lab_test_id, appointment=appointment)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def add_prescription(request, appointment_id):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    appointment = get_object_or_404(base_models.Appointment, appointment_id=appointment_id, doctor=doctor)
    serializer = PresicriptionSerilizer(data=request.data)

    if serializer.is_valid():
        serializer.save(appointment=appointment)
        return Response({'message': 'Prescription added successfully'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payments(request):
    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    payments = base_models.Billing.objects.filter(appointment__doctor=doctor, status='Paid')
    serializer = BillingSerializer(payments, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def notifications(request):
    from doctor.serializer import NotificationSerializer

    try:
        doctor = request.user.medicalprofessional
    except MedicalProfessional.DoesNotExist:
        return Response({'message': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    notifications = Notification.objects.filter(doctor=doctor, seen=False)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsDoctor])
def mark_notification_as_seen(request, id):
    try:
        doctor = request.user.medicalprofessional
        notification = Notification.objects.get(doctor=doctor, id=id)
        notification.seen = True
        notification.save()
        return Response({'message': 'Notification marked as seen'}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def doctor_profile(request):
    try:
        doctor = request.user.medicalprofessional
    except ObjectDoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoctorProfileSerializer(data=doctor)
    
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsDoctor])
def update_doctor_profile(request):
    try:
        doctor = request.user.medicalprofessional
    except ObjectDoesNotExist:
        return Response({'error': 'Doctor does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UpdateDoctorProfileSerializer(doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)