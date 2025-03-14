from django.urls import path
from .views import product_list, product_detail, submit_review  # ✅ Import submit_review view

urlpatterns = [
    path("", product_list, name="product_list"),  # ✅ View all products
    path("<int:product_id>/", product_detail, name="product_detail"),  # ✅ View a single product
    path("<int:product_id>/submit_review/", submit_review, name="submit_review"),  # ✅ Fix for NoReverseMatch error
]
