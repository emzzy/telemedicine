from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Patient(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=False)
    gender = models.CharField(max_length=15)
    location = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], null=True, blank=True)
    emergency_contact = models.TextField()
    #medical_information = models.FileField(upload_to='src/uploads/patient', null=True)
    #date_registered = models.DateTimeField(auto_now_add=True)
    is_active = True
    
    def __str__(self):
        return self.first_name
    
class MedicalProfessional(models.Model):
    title = models.CharField(max_length=50)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=15)
    medical_license = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9-]+$', # allows numbers, letters, and alphabets
                message="Medical license must contain only uppercase letters, numbers, or hyphens."
            )
        ],
        unique=True # no duplicate of license
    )
    specialty = models.CharField(max_length=100, default="Emergency Responder", null=True, blank=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    #professional_certificate = models.FileField(upload_to='', null=True)
    is_active = True
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class Appointments(models.Model):
    status_choices = [
        ('Pending'),
        ('Confirmed'),
        ('Completed'),
        ('Canceled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient', null=True, blank=True)
    medical_professional = models.ForeignKey(MedicalProfessional)
    date_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=status_choices, null=True, blank=True, default=None)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Your Appointment is on {self.date_time} with {self.medical_professional} for {self.patient.first_name} {self.patient.last_name}"

class Messages(models.Model):
    sender = models.ForeignKey()
    receiver = models.ForeignKey()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class VideoCallSession(models.Model):
    session_id = models.CharField(unique=True)
    patient = models.ForeignKey(Patient)
    medical_professional = models.ForeignKey(MedicalProfessional)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    status = models.TextChoices()
    notes = models.TextField(null=True, blank=True)

class Prescriptions(models.Model):
    patient = models.ForeignKey(Patient)
    MedicalProfessional = models.ForeignKey(MedicalProfessional)
    medication_name = models.CharField()
    dosage = models.CharField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    date_issued = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)

class MedicalRecords(models.Model):
    patients = models.ForeignKey(Patient)
    record_type = models.CharField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(blank=True, null=True)


class Notifications(models.Model):
    user = models.ForeignKey()
    message = models.CharField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Payments(models.Model):
    pass