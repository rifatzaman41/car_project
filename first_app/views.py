from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Car, Brand, Comment
from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Car, Order


@login_required
def buy_now(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        order = Order(user=request.user, car=car)
        order.save()
        return redirect('order-success')  # Redirect to a success page or order history
    else:
        return render(request, 'out_of_stock.html', {'car': car})  # Handle out of stock


def order_success(request):
    return render(request, 'order_success.html')


def home(request):
    cars = Car.objects.all()  # Assuming you want to display all cars
    return render(request, 'home.html', {'cars': cars})

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                messages.success(request, "Account created successfully")
                form.save()
                return redirect('home')  # Redirect after successful signup
        else:
            form = RegisterForm()
        return render(request, 'signup.html', {"form": form})
    else:
        return redirect('profile')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data["username"]
                userpass = form.cleaned_data["password"]
                user = authenticate(username=name, password=userpass)
                if user is not None:
                    login(request, user)
                    return redirect("profile")
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    else:
        return redirect('profile')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {"user": request.user})
    else:
        return redirect('login')


def user_logout(request):
    logout(request)
    return redirect('login')


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


class UserRegistrationView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
