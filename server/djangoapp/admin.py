from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
# CarModelAdmin class
admin.site.register(CarMake)
admin.site.register(CarModel)

# CarMakeAdmin class with CarModelInline

# Register models here
