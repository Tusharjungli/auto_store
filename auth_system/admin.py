from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# ✅ Check if User is already registered, and only register if it isn't
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass  # ✅ Ignore the error if User is already registered
