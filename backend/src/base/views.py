from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from doctor import models as doctor_model
from patient import models as patient_model
from base import models as base_models
from users import models as user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ServicesListSerializer
from django.shortcuts import get_object_or_404
from .serializers import BookAppointmentSerializer
from rest_framework import status
from decimal import Decimal


User = get_user_model()
class ServicesAPIView(APIView):
    pass

class ServicesListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Returns list of all available services"""
        services = base_models.Service.objects.all()
        serializer = ServicesListSerializer(services, many=True)
        
        return Response(serializer.data)

class ServiceDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        service = get_object_or_404(base_models.Service, pk=pk)
        #service = base_models.Service.objects.get(id=service_id)
        serializer = ServicesListSerializer(service)
        return Response(serializer.data)


class BookAppointment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, service_id, doctor_id):
        user_doctor = get_object_or_404(user_model.UserAccount, id=doctor_id)
        service = get_object_or_404(base_models.Service, id=service_id)
        doctor = get_object_or_404(doctor_model.MedicalProfessional, user=user_doctor)
        # get patient
        user_patient = request.user
        patient = get_object_or_404(patient_model.Patient, user=user_patient)
        
        update_patient_data = [
            'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'location'
        ]
        for field in update_patient_data:
            if field in request.data:
                setattr(user_patient, field, request.data[field])
        user_patient.save()

        # Update patient information if provided
        if 'gender' in request.data:
            patient.gender = request.data['gender']
        if 'address' in request.data:
            patient.address = request.data['address']
        if 'date_of_birth' in request.data:
            patient.date_of_birth = request.data['date_of_birth']
        patient.save()

        # Create appointment data
        appointment_data = {
            'service': service.id,
            'doctor': doctor.id,
            'patient': patient.id,
            'appointment_date': doctor.available_appointment_date,
            'issues': request.data.get('issues', ''),
            'symptoms': request.data.get('symptoms', ''),
            'status': 'Scheduled'
        }

        serializer = BookAppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            appointment = serializer.save()
            
            # Billing object
            billing = base_models.Billing.objects.create(
                patient=patient,
                appointment=appointment,
                sub_total=service.cost,
                tax=round(service.cost * Decimal('0.20'), 2),
                total=round(service.cost * Decimal('1.20'), 2),
                status='Unpaid'
            )
            print(request.data)
            return Response({
                'data': serializer.data,
                'appointment': serializer.data,
                'billing_id': billing.billing_id,
                'message': 'Appointment scheduled successfully!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, billing_id):
        billing = get_object_or_404(base_models.Billing, id=billing_id)
        
        return Response({
            'billing': billing,
        }, status=status.HTTP_200_OK)
