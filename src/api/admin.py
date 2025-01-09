from django.contrib import admin
from .models import Patient, MedicalProfessional

admin.site.register(Patient)
admin.site.register(MedicalProfessional)