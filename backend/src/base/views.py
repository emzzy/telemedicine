from django.shortcuts import render, redirect
from base import models as base_models
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from doctor import models as doctor_model
from patient import models as patient_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users import models as user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ServicesListSerializer
from django.shortcuts import get_object_or_404


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

    def get(self, request, service_id, doctor_id):
        pass

    def post(self, request, service_id, doctor_id):
        user = get_object_or_404(user_model.UserAccount, id=doctor_id)
        service = base_models.Service.objects.get(id=service_id)
        doctor = get_object_or_404(doctor_model.MedicalProfessional, user=user)
        patient = get_object_or_404(patient_model.Patient, user=request.user.is_patient)

        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            gender = request.POST.get('mobile')
            address = request.POST.get('first_name')
            date_of_birth = request.POST.get('dob')
            issues = request.POST.get('issues')
            symptoms = request.POST.get('symptoms')
            
            # Update patient bio data
            patient.full_name = full_name
            patient.email = email
            patient.mobile = mobile
            patient.gender = gender
            patient.address = address
            patient.date_of_birth = date_of_birth
            patient.save()
            
            # Appointment obj
            appointment = base_models.Appointment.objects.create(
                service = service,
                doctor=doctor,
                patient=patient,
                appointment_date=doctor.available_appointment_date,
                issues=issues,
                symptoms=symptoms
            )
            # Billing object
            billing = base_models.Billing()
            billing.patient = patient,
            billing.appointment = appointment,
            billing.sub_total = appointment.service.cost,
            billing.tax = appointment.service.cost * 20/100,
            billing.total = billing.sub_total + billing.tax
            billing.status = 'Unpaid'
            
            return redirect('checkout', billing.billing_id)
        
        context = {
            'service': service,
            'patient': patient,
            'doctor': doctor
        }
        return render(request, 'base/book_appointment.html', context)

