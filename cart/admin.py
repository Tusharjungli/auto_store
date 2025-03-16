from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

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

# ✅ OrderItem Inline (Allows viewing OrderItems inside Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Allow adding new OrderItems in the Order panel

# ✅ Order Admin (Manage Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")  # Allow filtering orders by status & date
    search_fields = ("id", "user__username")  # Allow searching orders by ID or username
    inlines = [OrderItemInline]  # Show OrderItems inside Order panel
    ordering = ("-created_at",)  # Show latest orders first

# ✅ OrderItem Admin (Manage Order Items separately)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "order", "quantity", "price")
    search_fields = ("product_name",)

# ✅ Register models
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)  # ✅ Register Order model
admin.site.register(OrderItem, OrderItemAdmin)  # ✅ Register OrderItem model
