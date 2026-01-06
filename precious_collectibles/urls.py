from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
import os

def privacy(request):
    
   return render(request, "privacy.html", {
       "logo": "media/privacy.jpeg"
   })

urlpatterns = [
    path('admin/', admin.site.urls),
    path("privacy.html", privacy, name="privacy_page"),
    path("api/v1/", include("api.urls", namespace="api_v1")),
    
]

if os.environ.get('DJANGO_SETTINGS_MODULE').rsplit('.', 1)[1] == 'local':
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
