# File location: finarva_ai/urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin import admin_site  # Import our custom admin site only once
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin_site.urls),  # Custom admin site
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('ai-assistant/', include('ai_assistant.urls')),
    path('', include('dashboard.urls')),  # Redirect root to dashboard
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)