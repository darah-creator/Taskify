from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .serializers import UserSerializer  # still useful for creating users


# ---------- SIGN UP ----------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        is_staff = request.POST.get("is_staff") == "on"  # checkbox for admin

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        user = User(username=username, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully! Please sign in.")
        return redirect("signin")

    return render(request, "signup.html")  # GET → show form


# ---------- SIGN IN ----------
def signin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # ✅ Redirect based on admin status
            if user.is_staff:
                return redirect("dashboard:admin_dashboard")  # admin dashboard
            else:
                return redirect("dashboard:user_dashboard")   # normal user dashboard

        else:
            messages.error(request, "Invalid credentials")
            return redirect("signin")

    return render(request, "signin.html")  # GET → show form


# ---------- SIGN OUT ----------
def signout_view(request):
    logout(request)
    messages.success(request, "You have been signed out successfully.")
    return redirect("signin")
