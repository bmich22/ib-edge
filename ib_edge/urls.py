from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('packages/', include('packages.urls')),
    path('contact/', include('contact.urls')),
    path('user_profile/', include('user_profiles.urls')),
    path('checkout/', include('checkout.urls')),
    path('tutoring_sessions/', include('tutoring_sessions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'ib_edge.views.handler404'
