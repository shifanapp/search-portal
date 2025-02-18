from django.db import models
from django_countries.fields import CountryField
from cities_light.models import City
from django.contrib.auth.models import User
from core.models import Category, Service  # Import the models from the core app

# Create your models here.

class Location(models.Model):
    country = CountryField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)



class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"UserDetails {self.id} - {self.user.username}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()  # Amount in cents
    payment_intent_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.status}"
