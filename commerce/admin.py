from django.contrib import admin
from .models import Categoria, Producto

from rest_framework.authtoken.models import Token, TokenProxy
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)