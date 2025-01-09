from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class UserAccountManager(BaseUserManager):
    """
    If you need custom user creation logic, define a BaseUserManager. 
    For example, you might want to handle user creation for Patient and MedicalProfessional
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.save(using=self.db)

        return user

class UserAccount(AbstractUser):
    """
    allows you to handle multiple user types (e.g., Patient and MedicalProfessional) 
    while maintaining Django's built-in authentication features.
    """
    is_patient = models.BooleanField(default=False)
    is_medical_professional = models.BooleanField(default=False)

    objects = UserAccountManager()

    groups = models.ManyToManyField(
        Group,
        related_name='useraccount_set',  # Custom reverse relation name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='useraccount_permissions',  # Custom reverse relation name
        blank=True
    )

    class Meta:
        db_table = 'api_useraccount'

    def __str__(self):
        return self.username

class Patient(AbstractUser):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='patient_profile', default=None)
    phone_number = models.CharField(max_length=15, blank=False)
    gender = models.CharField(max_length=15)
    location = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)], null=True, blank=True)
    emergency_contact = models.TextField(max_length=200, null=True, blank=True)
    medical_information = models.FileField(upload_to='src/uploads/patient', null=True)

    # Add related_name to groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        related_name='patient_set',  # Custom reverse relation name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='patient_permissions',  # Custom reverse relation name
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.username

class MedicalProfessional(AbstractUser):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='medical_profile', default=None)
    title = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=15)
    # medical_license = models.CharField(
    #     max_length=20,
    #     validators=[
    #         RegexValidator(
    #             regex=r'^[A-Z0-9-]+$', # allows numbers, letters, and alphabets
    #             message="Medical license must contain only uppercase letters, numbers, or hyphens."
    #         )
    #     ],
    #     unique=True # no duplicate of license
    # )
    specialty = models.CharField(max_length=100, default="Emergency Responder", null=True, blank=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    #professional_certificate = models.FileField(upload_to='', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_medical_professional = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name='medicalprofessional_set',  # Custom reverse relation name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='medicalprofessional_permissions',  # Custom reverse relation name
        blank=True
    )

    #objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username

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