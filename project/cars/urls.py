from django.urls import path
# from . import views
from .views import AdminUpdateCarView, CarListView, AddCarView, CarDetailView
# from .views import * _ იგივე

urlpatterns = [
    path('products/', CarListView.as_view(), name = 'car_list'),
    path('products/<int:pk>/', CarDetailView.as_view(), name = 'car_detail'),
    path('add/', AddCarView.as_view(), name = 'add_car'),
    path('products/<int:pk>/admin-update/', AdminUpdateCarView.as_view(), name = 'admin_update_car'),
]
