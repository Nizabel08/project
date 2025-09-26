# project/project/cars/urls.py
from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/add/', views.add_car, name='add_car'),
    path('car/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('car/<int:pk>/rent/', views.rent_car, name='rent_car'),
]
