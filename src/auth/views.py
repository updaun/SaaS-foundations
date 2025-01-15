from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
    return render(request, "auth/login.html", {})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Django Forms
        # user_exists = User.objects.filter(username__iexact=username).exists()
        # email_exists = User.objects.filter(email__iexact=email).exists()
        try:
            User.objects.create_user(username=username, email=email, password=password)
        except:
            pass
    return render(request, "auth/register.html", {})
