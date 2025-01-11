from django.contrib import admin
from .models import Patient, MedicalProfessional

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'gender', 'location')

admin.site.register(Patient, PatientAdmin)

admin.site.register(MedicalProfessional)