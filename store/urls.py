from django.urls import path
from .views import ai_search, product_detail, submit_review, product_list, track_order, update_order_status  # ✅ Import views

app_name = "store"  # ✅ Set namespace for future scalability

urlpatterns = [
    path("", product_list, name="product_list"),  # ✅ View all products
    path("<int:id>/", product_detail, name="product_detail"),  # ✅ View a single product
    path("<int:id>/submit_review/", submit_review, name="submit_review"),  # ✅ Handle reviews
    path("search/", ai_search, name="ai_search"),  # ✅ AI-powered search
    path('track-order/<uuid:tracking_id>/', track_order, name='track_order'),
    path('update-order-status/', update_order_status, name='update_order_status'),
]
