from django.contrib import admin
from doctor import models
from users.models import UserAccount
from djangoql.admin import DjangoQLSearchMixin


@admin.register(models.MedicalProfessional)
class DoctorAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('full_name', 'user', 'specialty', 'phone_number', 'years_of_experience')
    search_fields = ('user__phone_number', 'user__email', 'specialty')

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    full_name.admin_order_field = 'user__first_name'
    full_name.short_description = 'Full Name'


    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.admin_order_field = 'user__phone_number'
    phone_number.short_description = 'Phone Number'


    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'
    email.short_description = 'Email Address'


@admin.register(models.Notification)
class NotificationAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']
