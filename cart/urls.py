from django.urls import path
from .views import add_to_cart, remove_from_cart, cart_view, increase_quantity, decrease_quantity

urlpatterns = [
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),  # ✅ Add product to cart
    path("remove/<int:cart_item_id>/", remove_from_cart, name="remove_from_cart"),  # ✅ Remove item from cart
    path("increase/<int:cart_item_id>/", increase_quantity, name="increase_quantity"),  # ✅ Increase quantity
    path("decrease/<int:cart_item_id>/", decrease_quantity, name="decrease_quantity"),  # ✅ Decrease quantity
    path("", cart_view, name="cart_view"),  # ✅ View cart
]
