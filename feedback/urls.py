from django.urls import path
from .views import feedback_view, feedback_success, feedback_list  # ✅ Ensure all views are imported

urlpatterns = [
    path('', feedback_view, name='feedback_view'),  # ✅ Ensure the name matches templates
    path('success/', feedback_success, name='feedback_success'),  # ✅ Success page
    path('list/', feedback_list, name='feedback_list'),  # ✅ Add feedback list page
]
