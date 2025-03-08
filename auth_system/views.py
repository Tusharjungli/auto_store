from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    """ ✅ Handles user registration """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "auth_system/signup.html")

def login_view(request):
    """ ✅ Handles user login """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("homepage")  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, "auth_system/login.html")

def logout_view(request):
    """ ✅ Handles user logout """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("homepage")
