# store/admin.py
from django.contrib import admin
from .models import Product, Appointment

admin.site.register(Product)
admin.site.register(Appointment)