from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .models import Car
from .forms import CarForm



from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from .mixins import QueryParamsMixin
from django.conf import settings
import pdb
class CarListView(QueryParamsMixin, ListView) :
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        # pdb.set_trace()
        queryset = super().get_queryset() # queryset იყოს ცვლადი საიდაც super().get_queryset()-ით მიხვდება რომ Product-იდან მოგვაქვს მონაცემები
        
        query = self.request.GET.get('q')   # სახელის name-ით ძიება
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')  #  აქ მოდელის სახელს არ ვწერთ
        max_price = self.request.GET.get('max_price')

        #  რის მიხედვით გავფილტრო
        if query :
            queryset = queryset.filter(Q(name__icontains = query))  # სახელი შეიცავს query-ს

        if category :
            queryset = queryset.filter(category__name = category)

        if min_price :
            queryset = queryset.filter(price__gte = min_price) # greater or equal

        if max_price :
            queryset = queryset.filter(price__lte = max_price) # less or equeal
    
        # ordering
        order_by = self.request.GET.get('order_by') 
        if order_by in ['name', '-name', 'price', '-price', 'id', '-id'] :
            queryset = queryset.order_by(order_by)
        
        else :
            queryset = queryset.order_by('id')

        return queryset


class CarDetailView(DetailView) :
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()  

        recent = self.request.session.get('recent_cars', [])
        if car.id not in recent :  
            recent.append(car.id)

        recent = recent[-5:]    
        self.request.session['recent_cars'] = recent
        context['recent_cars'] = Car.objects.filter(id__in = recent).exclude(id = car.id)

        recent_cars = list(Car.objects.filter(id__in=recent))
        recent_cars_sorted = sorted(
            recent_cars, key=lambda x: recent.index(x.id), reverse=True
        )

        recent_cars_sorted = [p for p in recent_cars_sorted if p.id != car.id]

        context['recent_cars'] = recent_cars_sorted
        return context


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.contrib import messages
from django.core.mail import send_mail
class AddCarView(LoginRequiredMixin, CreateView) :
    model = Car
    form_class = CarForm
    template_name = 'cars/add_car.html'
    success_url = reverse_lazy('car_list')  
    
    def form_valid(self, form) :   
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'You have added a new car: {form.instance.name}')
        
        send_mail(
            subject='New Car',
            message= f'a new car {form.instance.name} was added by {self.request.user.username}',
            from_email='nizabel.japaridze1@gmail.com',
            recipient_list=['nizabel.japaridze1@gmail.com'],
            fail_silently=False,
        )
        return response


class AdminUpdateCarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView) :  # UserPassesTestMixin _ შევამოწმო იუზერი მფლობელია თუ ადმინი
    model = Car
    form_class = CarForm
    template_name = 'car/admin_update_car.html'
    context_object_name = 'car'

    # 
    def post(self, request, *args, **kwargs) :
        method = request.POST.get('_method', '').upper()  # იგივე რჩება
        if method != 'PUT' :
            return HttpResponseNotAllowed(['PUT'])  # რომელ მეთოდზე აქვს წვდომა/ დავბლოკეთ სხვა მეთოდები put-ის გარდა

        return super().post(request, *args, **kwargs)

    # არის თუ არა ადმინი დალოგინებული იუზერი
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated :  # დალოგინებული თუა
            return HttpResponseForbidden('Only admin can change the car qualities')
        return super().handle_no_permission()  # self-ის გარდა სხვა რამე რადგანაც არ გადაეცემა ფრჩხილები შეიძლება თავისუფალი დავტოვოთ

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs = {'pk' : self.object.pk})


