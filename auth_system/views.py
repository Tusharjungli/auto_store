from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "auth_system/signup.html", {"error": "Username already taken."})

        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect("login")

    return render(request, "auth_system/signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "auth_system/login.html", {"error": "Invalid credentials."})

    return render(request, "auth_system/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
