from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile
from .forms import ContactForm, UserProfileForm, UserUpdateForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            # Set a unique username, e.g. use email
            user.username = user_form.cleaned_data['email']
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('users:login')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_profile = UserProfile.objects.filter(phone_number=phone).first()
        if user_profile:
            user = user_profile.user
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
        return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
    else:
        form = ContactForm()
    return render(request, 'message/contact.html', {'form': form})
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=user_profile)

    # Get related data
    my_cars = request.user.cars.all()
    favorites = [f.car for f in request.user.favorites.select_related('car').all()]
    rentals = request.user.rentals.select_related('car').all()
    notifications = request.user.notifications.order_by('-created_at')[:20]

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'my_cars': my_cars,
        'favorites': favorites,
        'rentals': rentals,
        'notifications': notifications,
    })





