from .models import Car, CarLog
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender = Car) 
def log_product_creation(sender, instance, created, **kwargs) :
    if created :
        CarLog.objects.create(
            product = instance,
            message = f'product {instance.name} was created'  
        )
