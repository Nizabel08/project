from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf .urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acrs/', include('cars.urls')),
    path('users/', include('users.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login' ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
