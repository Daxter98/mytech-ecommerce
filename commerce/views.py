from django import template
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.http import Http404
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.views import View
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin

from xhtml2pdf import pisa

from .models import Categoria, Producto
from .serializers import ProductoSerializer, CategoriaSerializer


# Create your views here.
class IndexView(TemplateView):
    template_name='base.html'


class TopListaProductos(APIView):
    def get(sefl, request, format=None):
        productos = Producto.objects.all()[0:4]
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

class DetalleProducto(APIView):
    def get_object(self, categoria_slug, producto_slug):
        try:
            return Producto.objects.filter(categoria__slug=categoria_slug).get(slug=producto_slug)
        except Producto.DoesNotExist:
            raise Http404

    def get(self, request, categoria_slug, producto_slug, format=None):
        product = self.get_object(categoria_slug, producto_slug)
        serializer = ProductoSerializer(product)
        return Response(serializer.data)

class DetalleCategoria(APIView):
    def get_object(self, categoria_slug):
        try:
            return Categoria.objects.get(slug=categoria_slug)
        except Categoria.DoesNotExist:
            raise Http404
    
    def get(self, request, categoria_slug, format=None):
        categoria = self.get_object(categoria_slug)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

# function views

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        productos = Producto.objects.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    else:
        return Response({"productos": []})

class AlmacenPDFView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request, *args, **kwargs):
        template = get_template('admin/productos.html')

        productos = Producto.objects.all().order_by('categoria').values()
        total_existencias = Producto.objects.all().aggregate(total_stock=Sum('stock')).get('total_stock')

        context = {'title': 'Prueba 1', 'stock': productos, 'total': total_existencias}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf'

        pisaStatus = pisa.CreatePDF(html, dest=response)

        if pisaStatus.err:
            return HttpResponse('Problemas')
        
        return response