# project/project/cars/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

TRANSMISSION_CHOICES = [
    ('auto', 'ავტომატიკა'),
    ('manual', 'მექანიკა'),
    ('tiptronic', 'ტიპტრონიკი'),
]

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars", null=True, blank=True)
    available = models.BooleanField(default=True)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    city = models.CharField(max_length=50)
    fuel_capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class CarPhoto(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='car_pics/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Photo {self.order} for {self.car}"

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    city_rented_in = models.CharField(max_length=100)
    days = models.PositiveIntegerField()
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} rented by {self.renter} ({self.days} days)"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user} likes {self.car}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif for {self.user} - {'read' if self.read else 'unread'}"
