from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # If someone opens /accounts/login/, immediately redirect to your custom login view (/login/)
    path('accounts/login/', lambda request: redirect('login')),

    # Keep this AFTER the override so the redirect wins for /accounts/login/
    path('accounts/', include('django.contrib.auth.urls')),

    # core app routes (root)
    path('', include('core.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
