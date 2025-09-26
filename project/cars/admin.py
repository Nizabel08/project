from django.contrib import admin
from .models import Car


admin.site.site_header = "Car Rent🚗"
admin.site.site_title = "Car rent portal"
admin.site.index_title = 'Welcome to my car rent portal'

# cars/admin.py
from django.contrib import admin
from .models import Car, CarPhoto, Rental, Favorite, Notification

class CarPhotoInline(admin.TabularInline):
    model = CarPhoto
    extra = 0

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'city', 'available')
    inlines = [CarPhotoInline]

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('car', 'renter', 'days', 'price_paid', 'start_date')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user','car')
