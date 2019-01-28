from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('driver_reg/', views.driver_register),
    path('register/', views.register, name='register'),
    path('passenger_login/', views.passenger_login),
    path('passenger/', views.passenger_home),
    path('passenger/request/', views.make_request),
    path('passenger/request/edit/<int:ride_id>/', views.edit_request),
    path('passenger/request/delete/<int:ride_id>/', views.delete_request),

    path('passenger/join/', views.search_for_join),
    path('passenger/join/<int:ride_id>/', views.join),
    path('driver_login/', views.driver_login),
    path('driver/pickup/', views.search),
    path('driver/pickup/<int:ride_id>/', views.pickup),
    path('driver/finish/<int:ride_id>/', views.finish),
    path('driver/', views.driver_home),

    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html')),
    path('profile/', views.view_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
