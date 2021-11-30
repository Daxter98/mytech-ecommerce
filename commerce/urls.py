from os import name
from django.urls import path, include
from . import views

app_name='commerce'

urlpatterns=[
    path('', views.IndexView.as_view(), name='index'),  # backend entrypoint
    path('productos-recientes/', views.TopListaProductos.as_view(), name='latest'),
    path('productos/busqueda', views.search, name='buscar'),
    path('productos/<slug:categoria_slug>/<slug:producto_slug>/', views.DetalleProducto.as_view(), name='producto'),
    path('productos/<slug:categoria_slug>/', views.DetalleCategoria.as_view(), name='categorias'),
]