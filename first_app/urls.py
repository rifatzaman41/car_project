from django.urls import path
from .views import CarListView, CarDetailView, UserRegistrationView, UserProfileView
from .views import  CustomLoginView, CustomLogoutView
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('car-list/', CarListView.as_view(), name='car-list'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('buy/<int:car_id>/', views.buy_now, name='buy_now'),
    path('order-success/', views.order_success, name='order-success'),
    
]
