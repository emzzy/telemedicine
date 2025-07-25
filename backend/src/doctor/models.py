from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from users import models as user_model

#User = get_user_model()

NOTIFICATION_TYPE = (
    ('New Appointment', 'New Appointment'),
    ('Appointment Cancelled', 'Appointment Cancelled'),
)

def medicalprofessional_image_path(instance, filename):
    return f'medicalprofessional/{instance.user.id}/images/{filename}'


class MedicalProfessional(models.Model):
    user = models.OneToOneField(user_model.UserAccount, on_delete=models.CASCADE, related_name='medicalprofessional')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=medicalprofessional_image_path, null=True, blank=True)
    image_caption = models.CharField(max_length=100, default='profile picture')
    bio = models.CharField(max_length=100, null=True, blank=True)
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
    available_appointment_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    def __str__(self):
        return f'Dr. {self.user.first_name} {self.user.last_name}'


class Notification(models.Model):
    doctor = models.ForeignKey(MedicalProfessional, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey('base.Appointment', on_delete=models.CASCADE, null=True, blank=True, related_name='doctors_appointment_notification')
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Notification'

        def __str__(self):
            return f'Dr. {self.doctor.first_name} notification'