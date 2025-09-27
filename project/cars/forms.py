from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Car, CarPhoto, Rental

# Custom widget for multiple uploads
class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price_per_day', 'capacity', 'transmission', 'city', 'fuel_capacity']

class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price_per_day', 'capacity', 'transmission', 'city', 'fuel_capacity']
class CarPhotoForm(forms.Form):
    photos = forms.FileField(
        widget=MultiFileInput,
        required=False
    )
class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'days']
