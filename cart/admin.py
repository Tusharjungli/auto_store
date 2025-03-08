from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    """ ✅ Allows CartItems to be edited inside the Cart admin panel """
    model = CartItem
    extra = 1  # Show one empty form for new items

class CartAdmin(admin.ModelAdmin):
    """ ✅ Custom Admin Panel for Carts """
    list_display = ("id", "created_at")  # Show ID and creation date
    inlines = [CartItemInline]  # Show related cart items inline

class CartItemAdmin(admin.ModelAdmin):
    """ ✅ Custom Admin Panel for Cart Items """
    list_display = ("product", "cart", "quantity")

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
