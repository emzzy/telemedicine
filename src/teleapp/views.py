import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):

    # if request.user.is_authenticated:
    #     print(request.user.first_name)
    return HttpResponse("<h1> Currently building.......</h1>")


def pw_protected_view(request, *args, **kwargs):
    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
    
    is_allowed = False
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})


@login_required
def user_only_view(request, *args, **kwargs):
    print(request.user.is_staff)
    return render(request, "protected/user-only.html", {})

@login_required
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html")


def doctor_register_view(request, *args, **kwargs):
    return render(request, 'doctor-signup.html')

def patient_register_view(request, *args, **kwargs):
    return render(request, 'patient-signup.html')

