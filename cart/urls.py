from django.urls import path
from . import views  # ✅ Better readability

urlpatterns = [
    # 🛒 Cart Management
    path("", views.cart_view, name="cart_view"),  # ✅ View cart page
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),  # ✅ Add item to cart
    path("update/<int:product_id>/", views.update_cart, name="update_cart"),  # ✅ Update cart item quantity
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),  # ✅ Remove item from cart
    path("count/", views.get_cart_count, name="cart_count"),  # ✅ Get cart count
    
    # ✅ Order & Checkout
    path("checkout/", views.checkout, name="checkout"),  # ✅ Checkout page
    path("order-success/", views.order_success, name="order_success"),  # ✅ Order success page
    path("order-history/", views.order_history, name="order_history"),  # ✅ Order history page
    
    # 🚚 Order Tracking
    path("track/", views.track_order, name="track_order"),  # ✅ Track order page
]
