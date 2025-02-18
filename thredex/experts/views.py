from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .forms import LocationForm
from cities_light.models import City
from core.models import Service,Category
from django.conf import settings
import stripe
from .models import Payment, UserDetails  # Import the models
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Payment, UserDetails  # Import the models
import json
import requests
from django.contrib.auth import logout
from django.contrib import messages


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

# Check all cities
def basic_info(request):
    categories = Category.objects.all()
    services = Service.objects.all()
    form = LocationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Process the form (e.g., save data or create a user)
            return redirect('success_page')  # Redirect to a success page
        else:
            # Form is invalid, render the form with errors
            return render(request, 'experts/basic_info.html', {
                'form': form,
                'services': services,
                'categories': categories,
            })

    return render(request, 'experts/basic_info.html', {
        'form': form,
        'services': services,
        'categories': categories,
    })

def get_services(request, category_id):
    services = Service.objects.filter(category_id=category_id)
    service_list = [{'id': service.id, 'service_name': service.service_name} for service in services]
    return JsonResponse({'services': service_list})

def dashboard(request):
    return render(request, 'experts/expert_dashboard.html')

def expert_profile(request,user_id):
    user_details = get_object_or_404(UserDetails, user_id=user_id)
    print("user_details==",user_details)
    context = {
        'user_details': user_details,
    }
    return render(request, 'experts/expert_profile.html', context)

def load_cities(request):
    """
    AJAX endpoint to load cities based on the selected country.
    """
    country_code = request.GET.get('country')  # Get the country code from the AJAX request
    # print(f"Selected country code: {country_code}")  # Debugging purpose
    if country_code:
        cities = City.objects.filter(country__code2=country_code).order_by('name')
    else:
        cities = City.objects.none()

    # Return a JSON response with city data
    return JsonResponse({'cities': list(cities.values('id', 'name'))})

def get_currency_code(country_code):
    # Replace with the actual API endpoint and parameters
    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    response = requests.get(api_url)
    if response.status_code == 200:
        country_data = response.json()
        try:
            currencies = country_data[0]['currencies']
            currency_code = list(currencies.keys())[0]
            return currency_code
        except (KeyError, IndexError) as e:
            raise ValueError(f"Error extracting currency code: {e}")
    else:
        raise ValueError("Invalid country code or API error")

def get_exchange_rate(from_currency, to_currency):
    # Replace with the actual API endpoint and parameters
    api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(api_url)
    if response.status_code == 200:
        exchange_data = response.json()
        try:
            exchange_rate = exchange_data['rates'][to_currency]
            return exchange_rate
        except KeyError as e:
            raise ValueError(f"Error extracting exchange rate: {e}")
    else:
        raise ValueError("Invalid currency code or API error")

def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debugging line

            # Get the service amount from the Service table
            service = Service.objects.get(id=data.get('service'))
            amount_usd = float(service.price)  # Convert to float
            print(f"Service amount (in USD): {amount_usd}")  # Debugging line

            # Determine the currency based on the selected country
            country_code = data.get('country')
            currency = get_currency_code(country_code)
            print(f"Currency for country {country_code}: {currency}")  # Debugging line

            # Get the exchange rate from USD to the selected currency
            exchange_rate = get_exchange_rate('USD', currency)
            print(f"Exchange rate from USD to {currency}: {exchange_rate}")  # Debugging line

            # Convert the amount to the selected currency
            amount = int(amount_usd * exchange_rate * 100)  # Convert to cents
            print(f"Service amount (in {currency} cents): {amount}")  # Debugging line

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['card'],
            )
            print(f"PaymentIntent created: {intent}")  # Debugging line

            # Get or create the user in the auth_user table
            username = data.get('username')
            email = data.get('email')
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})

            # Save user details to the database
            category = Category.objects.get(id=data.get('category'))
            user_details = UserDetails.objects.create(
                user=user,
                full_name=data.get('full_name'),
                mobile_number=data.get('mobile_number'),
                whatsapp_number=data.get('whatsapp_number'),
                email=email,
                category=category,
                service=service,
                country=country_code,
                city=data.get('city'),
                area=data.get('area'),
                username=username
            )
            print("User details saved:", user_details)  # Debugging line
            Payment.objects.create(
                user=user,
                amount=amount,
                payment_intent_id=intent['id'],
                status='created',
            )
            print("Payment details saved")  # Debugging line

            return JsonResponse({'client_secret': intent['client_secret']})

        except Exception as e:
            print(f"Error creating payment intent: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
def submit_user_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})

            category = Category.objects.get(id=data.get('category'))
            service = Service.objects.get(id=data.get('service'))
            user_details = UserDetails.objects.get(
                user=user,
                full_name=data.get('full_name'),
                mobile_number=data.get('mobile_number'),
                whatsapp_number=data.get('whatsapp_number'),
                email=email,
                category=category,
                service=service,
                country=data.get('country'),
                city=data.get('city'),
                area=data.get('area'),
                username=username
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def payment_success(request):
    try:
        payment_intent_id = request.GET.get('payment_intent')
        payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        payment.status = 'succeeded'
        payment.save()
        return render(request, 'experts/expert_dashboard.html')
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment matching query does not exist.'}, status=404)    

def ajax_check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def get_service_price(request):
    service_id = request.GET.get('service_id')
    
    try:
        service = Service.objects.get(id=service_id)
        return JsonResponse({'price': service.price})  # Return the price in JSON format
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)

def logout_view(request):
    logout(request)
    response = redirect('home')  # Redirect to home page
    response.set_cookie('logout_success', 'true', max_age=5)  # Set temporary cookie for 5 seconds
    return response