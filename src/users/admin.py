from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from profiles.models import Patient, MedicalProfessional, UserAccount
from .forms import UserAccountChangeForm, UserAccountCreationForm

#User = get_user_model()

class UserAdminConfig(UserAdmin):
    model = UserAccount
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'location', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )
    
    # add_form = UserAccountCreationForm
    # form = UserAccountChangeForm
    # model = UserAccount
    # search_fields = ('email', 'first_name', 'last_name', 'type')
    # ordering = ('-email',)
    # list_display = (
    #     'email', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 
    #     'location', 'date_joined', 'is_active', 'is_staff', 'user_type',
    # )

admin.site.register(UserAccount, UserAdminConfig)
admin.site.register(Patient)
admin.site.register(MedicalProfessional)