from django.urls import path
from .views import cart_view, add_to_cart, update_cart, remove_from_cart
from cart.views import cart_view


urlpatterns = [
    path("", cart_view, name="cart_view"),  # ✅ View cart page
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),  # ✅ Add item to cart
    path("update/<int:product_id>/", update_cart, name="update_cart"),  # ✅ Update cart item quantity
    path("remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),  # ✅ Remove item from cart
    path('', cart_view, name='cart'),
]
