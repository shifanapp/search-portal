"""
URL configuration for thredex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    path('basic_info/', views.basic_info, name='basic_info'),
    path('experts/dashboard/', views.dashboard, name='expert_dashboard'),
    path('expert_profile/<int:user_id>/', views.expert_profile, name='expert_profile'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('get-services/<int:category_id>/', views.get_services, name='get_services'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('payment-success/', views.payment_success, name='payment_success'),
    #  path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('submit-user-details/', views.submit_user_details, name='submit_user_details'),
    # path('payment-success/', views.payment_success, name='payment_success'),
    path('ajax/check-username/', views.ajax_check_username, name='ajax_check_username'),
    path('get-service-price/', views.get_service_price, name='get_service_price'),
    # path('logout/', views.user_logout, name='logout')

    path('logout/', views.logout_view, name='logout'),




]



