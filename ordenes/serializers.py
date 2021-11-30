from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Orden, ArticuloOrden

from commerce.serializers import ProductoSerializer


class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticuloOrden
        fields = (
            "precio",
            "product",
            "cantidad",
        )

class OrdenSerializer(serializers.ModelSerializer):
    items = ArticuloSerializer(many=True)

    class Meta:
        model = Orden
        fields = (
            "id",
            "nombre_cliente",
            "apellido_cliente",
            "email",
            "direccion",
            "codigo_postal",
            "telefono",
            "stripe_token",
            "items",
        )
    
    def create(self, validated_data):
        datos_articulos = validated_data.pop('items')
        orden = Orden.objects.create(**validated_data)

        for datos in datos_articulos:
            ArticuloOrden.objects.create(orden=orden, **datos)

        return orden


class MisArticulosSerializer(serializers.ModelSerializer):
    product = ProductoSerializer()

    class Meta:
        model = ArticuloOrden
        fields = (
            "precio",
            "product",
            "cantidad",
        )

class MiOrdenSerializer(serializers.ModelSerializer):
    items = MisArticulosSerializer(many=True)

    class Meta:
        model = Orden
        fields = (
            "id",
            "nombre_cliente",
            "apellido_cliente",
            "email",
            "direccion",
            "codigo_postal",
            "telefono",
            "stripe_token",
            "items",
            "total"
        )