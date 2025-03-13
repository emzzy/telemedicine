from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

NOTIFICATION_TYPE = (
    ("Appointment Scheduled", "Appointment Scheduled"),
    ("Appointment Cancelled"), ("Appointment Cancelled"),
)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    image = models.FileField(upload_to='images', null=True, blank=True)
    location = models.TextField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='user_images')
    verified = models.BooleanField(default=False)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], null=True, blank=True)
    emergency_contact = models.TextField(max_length=200, null=True, blank=True)
    medical_information = models.FileField(upload_to='src/uploads/patient', null=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey('base.Appointment', on_delete=models.CASCADE, null=True, blank=True, related_name='patients_appointment_notification')
    type = models.CharField(max_length=100, choices=None)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notification'

        def __str__(self):
            return f"{self.patient.first_name}\'s notification"