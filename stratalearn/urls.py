from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.courses.urls')),
    path('api/', include('apps.learning.urls')),
    path('api/', include('apps.certificates.urls')),
    path('api/', include('apps.admin_dashboard.urls')),

    path('', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
