from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import geoip2.database
from django_countries import countries
import requests
from .models import Category,Service
from experts.models import UserDetails  # Assuming your user details are stored here
import pycountry
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


def get_country_name(country_code):
    """Convert country code to country name using pycountry."""
    try:
        return pycountry.countries.get(alpha_2=country_code).name
    except AttributeError:
        return country_code  # Return the code if it's invalid

def home(request):
    user_details = UserDetails.objects.order_by('-created_at')[:6]
    categories = Category.objects.order_by('priority')[:4]
    print(categories)
    # Convert country codes to country names
    for user in user_details:
        user.country_name = get_country_name(user.country)

    context = {
        'user_details': user_details,
        'categories' : categories,
    }
    return render(request, 'core/index.html', context)

def about(request):
    return render(request, 'core/about.html')
 
def contact(request):
    return render(request, 'core/contact.html')

def category_result(request,category_id):

    category = get_object_or_404(Category, id=category_id)
    # user_details = UserDetails.objects.filter(category=category)
    user_details = UserDetails.objects.filter(category_id=category_id).order_by('-created_at')
    # print(user_details.query.__str__(c)
    for user_detail in user_details:
        country_name = dict(countries).get(user_detail.country, user_detail.country)  # Convert code to name

   # Add Pagination: Show 10 users per page
    paginator = Paginator(user_details, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for user in user_details:
        country_obj = pycountry.countries.get(alpha_2=user.country)  # Get country name from code
    context = {
        'category': category,
        # 'user_details': user_details,
        'page_obj': page_obj,  # Send paginated results to the template
        'country_obj' : country_obj,

    }    
    return render(request, 'core/category_result.html',context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def search_expert(request):
    services = Service.objects.all()  # Fetch all services for the dropdown
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
        'services': services
    })

def get_cities(request):
    country_code = request.GET.get('country_code')
    query = request.GET.get('query', '')
    cities = []

    if country_code:
        try:
            geonames_url = "http://api.geonames.org/searchJSON"
            params = {
                'country': country_code,
                'name_startsWith': query,
                'featureClass': 'P',
                'maxRows': 10,
                'username': settings.GEONAMES_USERNAME,
            }
            response = requests.get(geonames_url, params=params)
            data = response.json()
            cities = [item['name'] for item in data.get('geonames', [])]
        except Exception as e:
            print(f"GeoNames Error: {e}")
    
    return JsonResponse({'cities': cities})

def search_users(request):
    # Get search parameters from GET request
    country = request.GET.get('country', '')
    city = request.GET.get('city', '')
    service = request.GET.get('service', '')
    area =  city
    print("area=====",area)
    # Filter UserDetails based on the search parameters
    users_qs = UserDetails.objects.all()
    if country:
        users_qs = users_qs.filter(country__icontains=country)
    if city:
        users_qs = users_qs.filter(city__icontains=city)
    if service:
        users_qs = users_qs.filter(service_id=service)
    if area:
        users_qs = users_qs.filter(area__icontains=area)
    # Prepare the result list
    results = []
    for user_detail in users_qs:
        country_name = dict(countries).get(user_detail.country, user_detail.country)  # Convert code to name
        results.append({
            'id': user_detail.user.id,  # Include the user ID
            'full_name': user_detail.user.get_full_name() or user_detail.user.username,
            'email': user_detail.user.email,
            'phone_number': user_detail.phone_number if hasattr(user_detail, 'phone_number') else '',
            'address': user_detail.address if hasattr(user_detail, 'address') else '',
            'country': country_name,  # Display full country name
            'city': user_detail.city,
            'service': user_detail.service.service_name if user_detail.service else '',
        })

    return JsonResponse({'results': results})

def signup(request):
    return render(request, 'core/signup.html')

def login(request):
    return render(request, 'core/login.html')
