import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):

    # if request.user.is_authenticated:
    #     print(request.user.first_name)
    return HttpResponse("<h1> Currently building.......</h1>")

@login_required
def user_only_view(request, *args, **kwargs):
    print(request.user.is_staff)
    return render(request, "protected/user-only.html", {})

@login_required
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html")

def user_register_view(request, *args, **kwargs):
    return render(request, 'signup.html')

def user_login(request, *args, **kwargs):
    return render(request, 'login.html')

def role_selector(request, *args, **kwargs):
    return render(request, 'role_selection.html')

# success page 
def success(request, *args, **kwargs):
    return render(request, 'success-page.html')

# dashboard after auth
def patient_dashboard(request, *args, **kwargs):
    return render(request, 'profils/patient-dashboard', {})

def med_pro_dashboard(request, *args, **kwargs):
    return render(request, 'profiles/doctor-dashboard', {})