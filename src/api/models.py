from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=False)
    gender = models.CharField(max_length=15)
    location = models.TextField()
    date_of_birth = models.DateField()
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    emergency_contact = models.TextField()
    #medical_information = models.FileField(upload_to='src/uploads/patient', null=True)
    is_active = True
    
    def __str__(self):
        return self.first_name
    
class MedicalProfessional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    specialty = models.CharField(max_length=100, default="Emergency Responder")
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    #professional_certificate = models.FileField(upload_to='', null=True)
    is_active = True
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
