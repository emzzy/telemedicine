from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserAccountManager
from django.utils.timezone import now


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        PATIENT = "PATIENT", "patient"
        MEDICALPROFESSIONAL = "MEDICALPROFESSIONAL", "medicalprofessional"
        ADMIN = "ADMIN", "admin"

    type = models.CharField(max_length=25, choices = Types.choices, null=True)

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.TextField(max_length=255, null=True, blank=True)
    date_joined = models.DateField(default=now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # special permission which define the patient and medical professional
    is_patient = models.BooleanField(default=False)
    is_medical_professional = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # defining the manager for UserAccount
    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        if self.is_superuser or self.is_admin:
            self.type = UserAccount.Types.ADMIN
        
        elif not self.type:
            self.type = UserAccount.Types.PATIENT
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'api_useraccount'


class Patient(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    location = models.TextField()
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], null=True, blank=True)
    emergency_contact = models.TextField(max_length=200, null=True, blank=True)
    medical_information = models.FileField(upload_to='src/uploads/patient', null=True)


class MedicalProfessional(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
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


class Appointments(models.Model):
    pass

class VideoCallSession(models.Model):
   pass

class Prescriptions(models.Model):
    pass

class MedicalRecords(models.Model):
    pass

class Messages(models.Model):
    pass

class Notifications(models.Model):
    pass

class Payments(models.Model):
    pass