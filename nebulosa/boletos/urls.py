from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendedor/', views.lista_boletos_venta, name='lista_boletos_venta'),
]