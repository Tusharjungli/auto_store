from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """ ✅ Custom user model extending Django's default User """
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users_groups",  # ✅ Custom related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users_permissions",  # ✅ Custom related_name to avoid conflict
        blank=True
    )

    def __str__(self):
        return self.username
