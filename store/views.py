# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from fuzzywuzzy import fuzz
from .models import Product
from .synonyms import SYNONYMS


def index(request):
    return render(request, 'index.html')


def products(request):
    products = Product.objects.all()
    categoria = request.GET.get('categoria', '')
    especie = request.GET.get('especie', '')
    nombre = request.GET.get('nombre', '')
    search_query = request.GET.get('search', '')

    if categoria:
        products = products.filter(categoria=categoria)
    if especie:
        products = products.filter(especie=especie)
    if nombre:
        products = products.filter(nombre__icontains=nombre)

    if search_query:
        scored_products = []
        search_query = search_query.lower().strip()
        expanded_query = []
        for word in search_query.split():
            expanded_query.append(word)
            for key, synonyms in SYNONYMS.items():
                if word in synonyms or word == key:
                    expanded_query.append(key)
                    expanded_query.extend(synonyms)
        expanded_query = list(set(expanded_query))

        for product in products:
            product_text = f"{product.nombre} {product.descripcion or ''} {product.categoria} {product.especie}".lower()
            max_score = 0
            for term in expanded_query:
                score = fuzz.partial_ratio(term, product_text)
                if score > max_score:
                    max_score = score
            if max_score > 60:
                scored_products.append((product, max_score))

        scored_products.sort(key=lambda x: x[1], reverse=True)
        products = [item[0] for item in scored_products]

    categorias = Product.objects.values_list('categoria', flat=True).distinct()
    especies = Product.objects.values_list('especie', flat=True).distinct()

    return render(request, 'products.html', {
        'products': products,
        'categorias': categorias,
        'especies': especies,
        'selected_categoria': categoria,
        'selected_especie': especie,
        'selected_nombre': nombre,
        'search_query': search_query,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': float(product.precio),
            'name': product.nombre,
        }

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, f"{product.nombre} ha sido añadido al carrito.")
    return redirect('products')


def cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    for product_id, item in cart.items():
        subtotal = item['quantity'] * item['price']
        total += subtotal
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'quantity': item['quantity'],
            'price': item['price'],
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def update_cart_quantity(request, product_id):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']
    product_id_str = str(product_id)

    if product_id_str in cart:
        action = request.POST.get('action')
        if action == 'increase':
            cart[product_id_str]['quantity'] += 1
        elif action == 'decrease' and cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, product_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        product_id_str = str(product_id)

        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, "Producto eliminado del carrito.")

    return redirect('cart')


def about(request):
    return render(request, 'about.html')


def appointments(request):
    if request.method == 'POST':
        # Lógica para citas (si la implementas después)
        pass
    return render(request, 'appointments.html')


def contact(request):
    if request.method == 'POST':
        # Lógica para contacto (si la implementas después)
        pass
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not all([username, email, password, password_confirm]):
            messages.error(request, "Por favor, completa todos los campos.")
            return render(request, 'register.html')

        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido(a).")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Error al registrar el usuario: {str(e)}")
            return render(request, 'register.html')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect('index')