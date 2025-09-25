from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')  
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True) 
    bio = models.TextField(blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s profile"         
       

