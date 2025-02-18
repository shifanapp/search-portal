from django.contrib import admin
from .models import Service,Category
from import_export.admin import ImportExportModelAdmin
from .models import Service
# Register your models here.

# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ['service_name', 'category', 'price', 'created_at']
#     list_filter = ['category']
#     search_fields = ['service_name', 'category__name']

admin.site.register(Category)



class ServiceAdmin(ImportExportModelAdmin):
    
    pass

admin.site.register(Service, ServiceAdmin)

