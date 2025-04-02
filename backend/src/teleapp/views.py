import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from base import models as base_models

this_dir = pathlib.Path(__file__).resolve().parent


def home_view(request, *args, **kwargs):
    services = base_models.Service.objects.all()
    context = {
        'services': services
    }
    return render(request, 'index.html', context)

@login_required
def user_only_view(request, *args, **kwargs):
    print(request.user.is_staff)
    return render(request, "protected/user-only.html", {})

@login_required
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html")

def user_register_view(request, *args, **kwargs):
    return render(request, 'auth/signup.html')

def user_login(request):
    return render(request, 'auth/login.html')

def user_logout(request):
    return render(request, 'logout.html', {})

def role_selector(request, *args, **kwargs):
    return render(request, 'auth/role_selection.html', {})

# success page 
def success(request, *args, **kwargs):
    return render(request, 'success-page.html')

# dashboard after auth
def patient_dashboard(request, *args, **kwargs):
    return render(request, 'profiles/patient-dashboard', {})

def med_pro_dashboard(request, *args, **kwargs):
    return render(request, 'profiles/doctor-dashboard', {})

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)
    context = {
        'service': service
    }
    return render(request, 'service_detail.html', context)