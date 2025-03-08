from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from auto_store.views import homepage  # ✅ Ensure homepage view is imported

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("auth_system.urls")),  # ✅ Authentication system (Login/Signup)
    path("products/", include("products.urls")),  # ✅ Products app
    path("cart/", include("cart.urls")),  # ✅ Shopping cart
    path("", homepage, name="homepage"),  # ✅ Homepage route
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
