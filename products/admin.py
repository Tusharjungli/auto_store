from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    """ ✅ Custom admin panel for managing products """
    list_display = ("name", "price", "is_featured")  # Show these columns in the admin panel
    list_filter = ("is_featured",)  # ✅ Add filter for featured products
    search_fields = ("name", "description")  # ✅ Enable search by product name & description

admin.site.register(Product, ProductAdmin)
