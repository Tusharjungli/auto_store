from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from auto_store.views import homepage, index # ✅ Ensure homepage view is imported
from store.views import  track_order
from uuid import UUID

urlpatterns = [
    path("admin/", admin.site.urls),
    path("store/", include("store.urls")),
    path("auth/", include("auth_system.urls")),  # ✅ Authentication system (Login/Signup)
    path("cart/", include("cart.urls")),  # ✅ Shopping cart
    path("", homepage, name="homepage"),  # ✅ Homepage route
    path('', index, name='index'),
    path('cart/', include('cart.urls')),
    path('feedback/', include('feedback.urls')),
    path('', include('chatbot.urls')),
    path("track-order/<int:tracking_id>/", track_order, name="track_order"),

]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
