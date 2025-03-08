from django.urls import path
from .views import product_list, product_detail

urlpatterns = [
    path("", product_list, name="product_list"),  # ✅ View all products
    path("<int:product_id>/", product_detail, name="product_detail"),  # ✅ View a single product
]
