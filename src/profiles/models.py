from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.TextField()
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], null=True, blank=True)
    emergency_contact = models.TextField(max_length=200, null=True, blank=True)
    medical_information = models.FileField(upload_to='src/uploads/patient', null=True)
    #user_type = UserAccount.Role.PATIENT


class MedicalProfessional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    medical_license = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9-]+$', # allows numbers, letters, and alphabets
                message="Medical license must contain only uppercase letters, numbers, or hyphens."
            )
        ],
        unique=True, null=True, blank=True
    )
    specialty = models.CharField(max_length=100, default="Emergency Responder", null=True, blank=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    professional_certificate = models.FileField(upload_to='', null=True, blank=True)
    #user_type = UserAccount.Role.MEDICALPROFESSIONAL
