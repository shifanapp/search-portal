from django.db import models
from django.utils import timezone

# Create your models here.
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional field for service description
    image_url = models.ImageField(upload_to='media',default="null",null=True)
    priority=models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)  # Manually define a default value
    updated_at = models.DateTimeField(auto_now=True)
    
    

    def __str__(self):
        return self.name

#Service Model
class Service(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Optional field for service description
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service_name} - {self.category.name}"