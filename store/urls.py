# store/urls.py
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)

app_urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('appointments/', views.appointments, name='appointments'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('', include(app_urlpatterns)),
    path('api/', include(api_urlpatterns)),
]