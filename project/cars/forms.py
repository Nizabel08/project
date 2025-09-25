from django import forms
from .models import Car

# model-based forma 
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'price', 'available']