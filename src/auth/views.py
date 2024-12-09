from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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

    return render(request, "auth/register.html", {})