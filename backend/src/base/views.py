from django.shortcuts import render
from base import models as base_models
from django.contrib.auth.decorators import login_required
from doctor import models as doctor_model
from patient import models as patient_model

# moved service listing to teleapp views

@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_model.MedicalProfessional.objects.get(id=doctor_id)
    patient = patient_model.Patient.objects.get(id=service_id)

    context = {
        'service': service
    }
    return render(request, 'book_appointment.html', context)