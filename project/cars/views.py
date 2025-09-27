from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import Car, CarPhoto, Favorite, Rental, Notification
from .forms import CarForm, CarPhotoForm, RentalForm, CarUpdateForm
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail


@login_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.owner != request.user:
        messages.error(request, "You do not have permission to edit this car.")
        return redirect('cars:car_detail', pk=pk)
    if request.method == 'POST':
        form = CarUpdateForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Car updated successfully.")
            return redirect('cars:car_detail', pk=car.pk)
    else:
        form = CarUpdateForm(instance=car)
    return render(request, 'cars/car_update.html', {'form': form, 'car': car})
# project/project/cars/views.py

class HomeView(generic.ListView):
    model = Car
    template_name = 'cars/home.html'
    context_object_name = 'cars'
    paginate_by = 3

    def get_queryset(self):
        qs = Car.objects.filter(available=True).order_by('-created_at')
        city = self.request.GET.get('city')
        if city:
            qs = qs.filter(city__icontains=city)
        year_min = self.request.GET.get('year_min')
        year_max = self.request.GET.get('year_max')
        if year_min:
            qs = qs.filter(year__gte=int(year_min))
        if year_max:
            qs = qs.filter(year__lte=int(year_max))
        capacity = self.request.GET.get('capacity')
        if capacity:
            qs = qs.filter(capacity=int(capacity))
        return qs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve filtering params in pagination links
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            get_params.pop('page')
        context['querystring'] = get_params.urlencode()
        return context

class CarDetailView(generic.DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        photo_form = CarPhotoForm(request.POST, request.FILES)
        if form.is_valid() and photo_form.is_valid():
            with transaction.atomic():
                car = form.save(commit=False)
                car.owner = request.user
                car.save()
                files = request.FILES.getlist('photos')
                if files:
                    for idx, f in enumerate(files):
                        CarPhoto.objects.create(car=car, image=f, order=idx)
            send_mail(
                subject='New Product',
                message=(
                    f'A new car {car.brand} {car.model} ({car.year}) was added by {request.user.username}'
                ),
                from_email='sender.example@gmail.com',
                recipient_list=['recipient.example@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Car added successfully.")
            return redirect('users:profile')
        else:
            return render(request, 'cars/add_car.html', {'form': form, 'photo_form': photo_form})
    else:
        form = CarForm()
        photo_form = CarPhotoForm()
        return render(request, 'cars/add_car.html', {'form': form, 'photo_form': photo_form})

@login_required
def toggle_favorite(request, pk):
    car = get_object_or_404(Car, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, car=car)
    if not created:
        fav.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites.")
    return redirect(request.META.get('HTTP_REFERER', reverse('cars:car_detail', kwargs={'pk': pk})))

@login_required
def rent_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if not car.available:
        messages.error(request, "This car is currently not available.")
        return redirect('cars:car_detail', pk=pk)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.renter = request.user
            rental.city_rented_in = car.city
            rental.price_paid = car.price_per_day * rental.days
            rental.end_date = rental.start_date + timedelta(days=rental.days)
            rental.save()
            car.available = False
            car.save()
            Notification.objects.create(
                user=car.owner,
                message=f"Your car {car} was rented by {request.user.username} for {rental.days} days."
            )
            messages.success(request, f"Car rented successfully. Total: {rental.price_paid}. You can view your rental details on your profile page.")
            return redirect('users:profile')
        else:
            messages.error(request, "Rental form is invalid. Please check your input.")
            return render(request, 'cars/rent_car.html', {'car': car, 'form': form})
    else:
        form = RentalForm(initial={'start_date': timezone.localdate()})
    return render(request, 'cars/rent_car.html', {'car': car, 'form': form})

@login_required
def user_profile(request):
    user = request.user
    profile = user.userprofile
    my_cars = user.cars.all()
    favorites = [f.car for f in user.favorites.select_related('car').all()]
    rentals = user.rentals.select_related('car').all()
    notifications = user.notifications.order_by('-created_at')[:20]
    return render(request, 'users/profile.html', {
        'profile': profile,
        'my_cars': my_cars,
        'favorites': favorites,
        'rentals': rentals,
        'notifications': notifications,
    })
