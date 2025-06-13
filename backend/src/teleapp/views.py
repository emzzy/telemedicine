import pathlib
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base import models as base_models


this_dir = pathlib.Path(__file__).resolve().parent


def home_view(request, *args, **kwargs):
    return render(request, 'index.html')

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
    #service = base_models.Service.objects.get(id=service_id)
    service = get_object_or_404(base_models.Service, id=service_id)
    doctors = service.available_doctors.filter(is_medical_professional=True)
    
    context = {
        'service': service,
        'doctors': doctors
    }
    return render(request, 'service.html', context)