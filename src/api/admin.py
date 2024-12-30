from django.contrib import admin
from .models import Patient, MedicalProfessional


# Register your models here.
admin.site.register(Patient)
admin.site.register(MedicalProfessional)