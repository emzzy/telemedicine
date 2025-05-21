from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth import get_user_model
from doctor import models as doctor_model
from patient import models as patient_model

User = get_user_model()

class Service(models.Model):
    """properties for each available service """
    from users.models import UserAccount
    from doctor.models import MedicalProfessional
    image = models.FileField(upload_to='images', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(UserAccount, limit_choices_to={'is_medical_professional': True}, blank=True)
    doctor_details = models.ManyToManyField(MedicalProfessional, blank=True)

    def get_doctors_by_location(self, patient_location):
        """returns a list of doctors in the same location as the patient"""
        return self.available_doctors.filter(location=patient_location)
    
    def __str__(self):
        return f'{self.name} - {self.cost}'


class Appointment(models.Model):
    STATUS = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled')
    ]
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_app')
    doctor = models.ForeignKey(doctor_model.MedicalProfessional, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors_appointment_notification')
    patient = models.ForeignKey(patient_model.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_appointment_notification')
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True) 
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet='1234567890')
    status = models.CharField(max_length=120, choices=STATUS)

    def __str__(self):
        return f'{self.patient.user.first_name} with {self.doctor.user.first_name}'
    

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField

    def __str__(self):
        return f'Medical record for {self.appointment.patient.full_name}'
    

class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Prescription for {self.appointment.patient.full_name}'
    

class Billing(models.Model):
    patient = models.ForeignKey(patient_model.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='billing_for_patient')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Billing for {self.patient.full_name} - Total: {self.total}'
    