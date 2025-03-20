from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    """ ✅ Custom admin panel for managing products """
    
    list_display = ("name", "price", "stock", "is_featured", "created_at")  # ✅ Show stock & date
    list_filter = ("is_featured", "created_at")  # ✅ Filter by featured & date
    search_fields = ("name", "description")  # ✅ Enable search by product name & description
    list_editable = ("price", "stock", "is_featured")  # ✅ Allow inline editing
    readonly_fields = ("created_at",)  # ✅ Prevent manual editing of created_at
    ordering = ("-created_at",)  # ✅ Show newest products first

admin.site.register(Product, ProductAdmin)
