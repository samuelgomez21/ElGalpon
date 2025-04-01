# store/admin.py
from django.contrib import admin
from .models import Producto, CitaVeterinaria, Cliente, Empleado, Venta, DetalleVenta

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'especie', 'precio', 'stock', 'fecha_ingreso')
    list_filter = ('categoria', 'especie')
    search_fields = ('nombre', 'descripcion')

@admin.register(CitaVeterinaria)
class CitaVeterinariaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_hora', 'motivo', 'estado')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('cliente__nombre', 'motivo')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'email')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'horario_entrada', 'horario_salida')
    list_filter = ('cargo',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total')
    list_filter = ('fecha',)
    search_fields = ('cliente__nombre',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'subtotal')
    list_filter = ('venta',)
    search_fields = ('producto__nombre',)