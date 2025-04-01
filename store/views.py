# store/views.py
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Producto, CitaVeterinaria
from .serializers import ProductoSerializer
from .forms import CitaVeterinariaForm

# Vistas HTML
def index(request):
    return render(request, 'index.html')

def products(request):
    productos = Producto.objects.all()
    return render(request, 'products.html', {'products': productos})

def cart(request):
    return render(request, 'cart.html')

def appointments(request):
    if request.method == 'POST':
        form = CitaVeterinariaForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'appointments.html', {
                'form': CitaVeterinariaForm(),
                'success': True,
                'appointments': CitaVeterinaria.objects.all()
            })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CitaVeterinariaForm()
    return render(request, 'appointments.html', {
        'form': form,
        'appointments': CitaVeterinaria.objects.all()
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Vistas API
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = []