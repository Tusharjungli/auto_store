from django.contrib import admin
from .models import Product  # ✅ Import Product model

admin.site.register(Product)  # ✅ Register the model
