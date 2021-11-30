from django.urls import path
from django.urls import path
from ordenes import views

urlpatterns = [
    path('pagar/', views.pagar, name='pago'),
    path('ordenes/', views.ListaOrdenes.as_view(), name='listado')
]
