from django.contrib import admin

from doctor import models


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialty', 'qualification', 'years_of_experience']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']


admin.site.register(models.MedicalProfessional, DoctorAdmin)
admin.site.register(models.Notification, NotificationAdmin)
