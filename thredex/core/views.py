from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import geoip2.database
from django_countries import countries  # To get the list of countries
import requests
# Create your views here.

def home(request):
    return render(request, 'core/home.html')

# Helper: Get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # For localhost, use a known public IP for testing
    return ip

# Main view for search page
def search_expert(request):
    default_country = "US"  # Fallback country code
    current_country = default_country

    try:
        ip = get_client_ip(request)
        with geoip2.database.Reader(f"{settings.GEOIP_CITY_PATH}") as reader:
            response = reader.city(ip)
            current_country = response.country.iso_code
    except Exception as e:
        print(f"GeoIP2 Error: {e}")
    
    return render(request, 'core/search_expert.html', {
        'countries': countries,
        'current_country': current_country,
    })

# Fetch cities based on the selected country using GeoNames
def get_cities(request):
    country_code = request.GET.get('country_code')
    query = request.GET.get('query', '')  # For filtering by user input
    cities = []

    if country_code:
        try:
            geonames_url = f"http://api.geonames.org/searchJSON"
            params = {
                'country': country_code,
                'name_startsWith': query,
                'featureClass': 'P',  # Only cities
                'maxRows': 10,
                'username': settings.GEONAMES_USERNAME,
            }
            response = requests.get(geonames_url, params=params)
            data = response.json()

            # Extract city names from GeoNames response
            cities = [item['name'] for item in data.get('geonames', [])]
        except Exception as e:
            print(f"GeoNames Error: {e}")
    
    return JsonResponse({'cities': cities})

def signup(request):
    return render(request, 'core/signup.html')

def login(request):
    return render(request, 'core/login.html')