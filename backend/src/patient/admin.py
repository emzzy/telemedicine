from django.contrib import admin
from patient import models
from djangoql.admin import DjangoQLSearchMixin


admin.register(models.Patient)
class PatientAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ['user', 'full_name', 'age']


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type', 'seen', 'date']