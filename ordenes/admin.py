from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Orden, ArticuloOrden

# Register your models here.
admin.site.register(Orden)
admin.site.register(ArticuloOrden)


class MyAdminSite(AdminSite):
    pass