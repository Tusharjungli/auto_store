from django.contrib import admin
from django.urls import path, include
from auto_store.views import homepage  # ✅ Import the homepage view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # ✅ Admin Panel
    path("auth/", include("auth_system.urls")),  # ✅ Authentication System (Login/Signup)
    path("products/", include("products.urls")),  # ✅ Product Pages
    path("cart/", include("cart.urls")),  # ✅ Shopping Cart
    path("", homepage, name="home"),  # ✅ Homepage Route
]

# ✅ Serve media files (product images) in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
