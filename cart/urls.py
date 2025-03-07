from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, increase_quantity, decrease_quantity, clear_cart

urlpatterns = [
    path("", cart_view, name="cart_view"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    path("increase/<int:product_id>/", increase_quantity, name="increase_quantity"),  # ✅ Increase quantity
    path("decrease/<int:product_id>/", decrease_quantity, name="decrease_quantity"),  # ✅ Decrease quantity
    path("clear/", clear_cart, name="clear_cart"),
]
