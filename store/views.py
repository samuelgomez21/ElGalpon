# store/views.py
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .forms import AppointmentForm

# Vistas HTML
def index(request):
    return render(request, 'index.html')

def products(request):
    return render(request, 'products.html')

def cart(request):
    return render(request, 'cart.html')

def appointments(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'appointments.html', {'form': AppointmentForm(), 'success': True})
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = AppointmentForm()
    return render(request, 'appointments.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Vistas API
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []