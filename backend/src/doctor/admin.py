from django.contrib import admin
from doctor import models
from users.models import UserAccount

#admin.site.unregister(models.MedicalProfessional)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'specialty', 'phone_number', 'years_of_experience')
    search_fields = ('user__phone_number', 'user__email', 'specialty')

    def full_name(self, obj):
        """fetch first_name and last_name from the default model"""
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


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']


admin.site.register(models.MedicalProfessional, DoctorAdmin)
admin.site.register(models.Notification, NotificationAdmin)
