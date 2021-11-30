from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Categoria, Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'get_absolute_url',
            'descripcion',
            'precio',
            'get_image',
            'get_miniatura',
            'fecha_entrada',
            'stock'
        )

class CategoriaSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True)

    class Meta:
        model = Categoria
        fields = (
            'id',
            'nombre',
            'get_absolute_url',
            'productos',
        )