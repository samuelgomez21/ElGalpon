# store/urls.py
from django.urls import path, include
from . import views
from rest_framework import routers

# Configuración de la API con Django REST Framework
router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

# Rutas para las vistas HTML
app_urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('appointments/', views.appointments, name='appointments'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

# Rutas para la API
api_urlpatterns = [
    path('', include(router.urls)),
]

# Combinar todas las rutas
urlpatterns = [
    path('', include(app_urlpatterns)),
    path('api/', include(api_urlpatterns)),
]