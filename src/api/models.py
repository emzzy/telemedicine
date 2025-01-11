from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email address")
            
        email = self.normalize_email(email).lower()

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_admin(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    allows you to handle multiple user types (e.g., Patient and MedicalProfessional) 
    while maintaining Django's built-in authentication features.
    """
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_patient = models.BooleanField(default=False)
    is_medical_professional = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'api_useraccount'

    def __str__(self):
        return self.username

class Patient(AbstractUser):
    pass

class MedicalProfessional(AbstractUser):
    pass

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