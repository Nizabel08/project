from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login_direct'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact_view, name='contact'),
    # path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
]
