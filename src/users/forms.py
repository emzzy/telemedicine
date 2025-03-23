from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from profiles.models import UserAccount


class UserAccountCreationForm(UserCreationForm):
     
     class Meta:
            model = UserAccount
            fields = ['email', 'first_name', 'last_name', 'password', 'phone_number', 'gender', 'date_of_birth', 'location']

# to modify user's acccount
class UserAccountChangeForm(UserChangeForm):
     
     class Meta:
            model = UserAccount
            fields = ['email', 'first_name', 'last_name']

# to update patient details after signup
# class PatientForm(forms.modelfor):
#       class Meta:
#             model = Patient
#             fields = ['location', 'age', 'emergency_contact', 'medical_information']

# to update medical professional details after signup
# class MedicalProfessionalForm(forms.ModelForm):
#       class Meta:
#             model = MedicalProfessional
#             fields = ['title', 'medical_license', 'specialty', 'years_of_experience', 'professional_certificate']
