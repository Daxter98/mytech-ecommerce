from re import L
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import ExtractDay
from django.db import models

from commerce.models import Producto

# Create your models here.
class Orden(models.Model):
    user = models.ForeignKey(User, related_name='ordenes', on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=100, default='')
    telefono = models.CharField(max_length=100)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100, default='')

    class Meta: 
        ordering = ['-fecha_orden',]
        verbose_name_plural = 'Ordenes'
    
    def __str__(self) -> str:
        return self.nombre_cliente


    @classmethod
    def get_reporte_ventas(cls):
        ventas = cls.objects.annotate(
            day=ExtractDay('fecha_orden')
        ).values('total', 'day')

        data = {}      
        for venta in ventas: 
            if venta['day'] not in data: 
                data[venta['day']] = venta['total']
            else: 
                data[venta['day']] += venta['total']
        
        labels = list(data.keys())

        return data, labels

class ArticuloOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, related_name='items', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Articulos de Ordenes'

    def __str__(self) -> str:
        return '%s' % self.id