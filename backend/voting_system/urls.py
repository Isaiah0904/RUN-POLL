"""voting_system URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Serve HTML pages at root
    path('elections/', include('elections.urls')),  # Elections pages and API
    path('notifications/', include('notifications.urls')),  # Notifications pages and API
    path('voting/', include('voting.urls')),  # Voting pages and API
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)