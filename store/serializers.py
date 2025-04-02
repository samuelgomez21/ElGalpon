# store/serializers.py
from rest_framework import serializers
from .models import Product

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'nombre', 'categoria', 'especie', 'precio', 'stock', 'descripcion', 'fecha_ingreso', 'imagen']