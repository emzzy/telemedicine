from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserAccount

class UserAccountCreationForm(UserCreationForm):
     
     class Meta:
            model = UserAccount
            fields = ['email', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'location']


class UserAccountChangeForm(UserChangeForm):
     
     class Meta:
            model = UserAccount
            fields = ['email', 'first_name', 'last_name']