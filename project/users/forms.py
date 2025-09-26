from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, UserProfile

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'city', 'avatar']
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)



class UserProfileForm(forms.ModelForm) :
    class Meta :   # model form-ს ვქმნი და მეტა მშობელ კლასად რომ წარმოიდგინოს
        model = UserProfile
        fields = ['phone_number']


class UserUpdateForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ['first_name', 'last_name', 'email', 'password'] 