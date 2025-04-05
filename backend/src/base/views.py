from django.shortcuts import render, redirect
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

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('mobile')
        address = request.POST.get('first_name')
        dob = request.POST.get('dob')
        issues = request.POST.get('issues')
        symptoms = request.POST.get('symptoms')

        # Update patient bio data
        patient.first_name = first_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.dob = dob
        patient.save()
        
        # Appointment obj
        appointment = base_models.Appointment.objects.create(
            service = service,
            doctor=doctor,
            patient=patient,
            new_appointment_date=doctor.available_appointment_date,
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
    return render(request, 'book_appointment.html', context)

