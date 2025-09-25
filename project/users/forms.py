from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)



class UserProfileForm(forms.ModelForm) :
    class Meta :   # model form-ს ვქმნი და მეტა მშობელ კლასად რომ წარმოიდგინოს
        model = UserProfile
        fields = ['profile_picture', 'bio', 'birth_date', 'phone_number']


class UserUpdateForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ['first_name', 'last_name', 'email', 'password'] 