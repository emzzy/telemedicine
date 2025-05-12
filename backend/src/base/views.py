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
        user = get_object_or_404(user_model.UserAccount, id=doctor_id)
        service = get_object_or_404(base_models.Service, id=service_id)
        doctor = get_object_or_404(doctor_model.MedicalProfessional, user=user)
        patient = get_object_or_404(patient_model.Patient, user=request.user)
        
        data = request.data.copy()
        data['service'] = service.id
        data['doctor'] = doctor.id
        data['patient'] = patient.id
        data['appointment_date'] = doctor.available_appointment_date

        queryset = base_models.Appointment.objects.all()
        serializer = BookAppointmentSerializer(data=data)
        if serializer.is_valid():
            appointment = serializer.save()
            
            # Billing object
            billing = base_models.Billing.objects.create(
                patient=patient,
                appointment=appointment,
                sub_total=service.cost,
                tax=round(service.cost * 0.20, 2),
                total=round(service.cost * 1.20, 2),
                status='Unpaid'
            )            
            return Response({
                'appointment': serializer.data,
                'billing_id': billing.billing_id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
