from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta: #table-is saxeli mxolobitshi 
        verbose_name = 'Car' #mxolobiti
        verbose_name_plural = 'Car' #mravlobiti


class CarLog(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'log for {self.car.name} : {self.message[:30]}'
    


class CarLog(models.Model) :
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'log for {self.car.name} : {self.message[:30]}' # slicing
    




