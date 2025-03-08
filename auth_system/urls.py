from django.urls import path
from .views import signup_view, login_view, logout_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),  # ✅ User Registration
    path("login/", login_view, name="login"),  # ✅ User Login
    path("logout/", logout_view, name="logout"),  # ✅ User Logout
]
