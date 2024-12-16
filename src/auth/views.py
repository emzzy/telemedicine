from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == "POST":
        password = request.POST.get("password") or None
        username = request.POST.get("username") or None
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to a success page
                print("Login Here!")
                return redirect("/")
    return render(request, "auth/login.html", {})


def register_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username", "") or None
        first_name = request.POST.get("first_name", "") or None
        last_name = request.POST.get("last_name", "") or None
        password = request.POST.get("password", "") or None
        email = request.POST.get("email") or None
        #phone_number = request.POST.get("phone_number", "") or None
        #user_exists = User.objects.filter(username__iexact=email).exists()
        try:
            User.objects.create_user(username, first_name=first_name, last_name=last_name, password=password, email=email)
        except:
            pass
    return render(request, "auth/register.html", {})