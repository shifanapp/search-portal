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
    path('', views.home, name='home'),          # Homepage
    path('search/', views.search_expert, name='search_expert'),
    # path('get-location-suggestions/', views.get_location_suggestions, name='get_location_suggestions'),
    # path('get_location_suggestions', views.get_location_suggestions, name='get_location_suggestions'),
    path('get-cities/', views.get_cities, name='get_cities'),  # URL for the AJAX call
    path('signup/', views.signup, name='signup'),  
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # path('category_result/', views.category_result, name='category_result'),
     path('category/<int:category_id>/', views.category_result, name='category_result'),


    path('search-users/', views.search_users, name='search_users'),


    # path('about/', views.about, name='about'),   # About Page
    # path('contact/', views.contact, name='contact'), # Contact Page
]
