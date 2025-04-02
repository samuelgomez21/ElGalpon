# store/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Producto, CitaVeterinaria, Cliente
from .serializers import ProductoSerializer
from .forms import CitaVeterinariaForm, UserRegisterForm, UserLoginForm  # Importamos los formularios aquí
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Vistas HTML
def index(request):
    productos_destacados = Producto.objects.all().order_by('-id')[:4]
    return render(request, 'index.html', {
        'productos_destacados': productos_destacados
    })

def products(request):
    productos = Producto.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        productos = productos.filter(
            Q(nombre__icontains=search_query) | Q(descripcion__icontains=search_query)
        )

    categoria = request.GET.get('categoria', '')
    especie = request.GET.get('especie', '')
    if categoria:
        productos = productos.filter(categoria=categoria)
    if especie:
        productos = productos.filter(especie=especie)

    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        productos = productos.order_by('precio')
    elif sort_by == 'price_desc':
        productos = productos.order_by('-precio')

    ganaderia = productos.filter(especie__in=['vacas', 'caballos', 'terneros'])
    porcicultura = productos.filter(especie='cerdos')
    avicultura = productos.filter(especie__in=['pollos', 'gallinas'])
    mascotas = productos.filter(especie__in=['perros', 'gatos', 'otros'])

    paginator_ganaderia = Paginator(ganaderia, 12)
    paginator_porcicultura = Paginator(porcicultura, 12)
    paginator_avicultura = Paginator(avicultura, 12)
    paginator_mascotas = Paginator(mascotas, 12)

    page_number = request.GET.get('page', 1)
    page_ganaderia = paginator_ganaderia.get_page(page_number)
    page_porcicultura = paginator_porcicultura.get_page(page_number)
    page_avicultura = paginator_avicultura.get_page(page_number)
    page_mascotas = paginator_mascotas.get_page(page_number)

    return render(request, 'products.html', {
        'ganaderia': page_ganaderia,
        'porcicultura': page_porcicultura,
        'avicultura': page_avicultura,
        'mascotas': page_mascotas,
        'search_query': search_query,
        'selected_categoria': categoria,
        'selected_especie': especie,
        'selected_sort': sort_by,
        'categorias': Producto.CATEGORIA_CHOICES,
        'especies': Producto.ESPECIE_CHOICES,
        'page_ganaderia': page_ganaderia,
        'page_porcicultura': page_porcicultura,
        'page_avicultura': page_avicultura,
        'page_mascotas': page_mascotas,
    })

def cart(request):
    return render(request, 'cart.html')

@login_required
def appointments(request):
    if request.method == 'POST':
        form = CitaVeterinariaForm(request.POST)
        if form.is_valid():
            # Buscar el cliente asociado al usuario autenticado
            try:
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                # Si no existe un cliente asociado, creamos uno
                cliente = Cliente.objects.create(
                    user=request.user,
                    nombre=request.user.first_name,
                    email=request.user.email,
                    telefono='',  # Puedes ajustar esto si tienes un campo en el formulario de registro
                    direccion=''  # Puedes ajustar esto si tienes un campo en el formulario de registro
                )

            cita = form.save(commit=False)
            cita.cliente = cliente
            cita.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'appointments.html', {
                'form': CitaVeterinariaForm(),
                'success': True,
                'appointments': CitaVeterinaria.objects.filter(cliente__user=request.user)
            })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'appointments.html', {
                'form': form,
                'success': False,
                'appointments': CitaVeterinaria.objects.filter(cliente__user=request.user)
            })
    else:
        form = CitaVeterinariaForm()
    return render(request, 'appointments.html', {
        'form': form,
        'appointments': CitaVeterinaria.objects.filter(cliente__user=request.user)
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Vistas de autenticación
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(
                user=user,
                nombre=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono'],
                direccion=form.cleaned_data['direccion']
            )
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
def logout_user(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión!')
    return redirect('index')

# Vistas API
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = []