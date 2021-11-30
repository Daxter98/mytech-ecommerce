from re import template
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.views.generic.base import View
from django.template.loader import get_template
from django.http.response import HttpResponse

from rest_framework import serializers, status, authentication, permissions
from rest_framework import response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from stripe.api_resources import source

from xhtml2pdf import pisa

from .models import Orden, ArticuloOrden
from .serializers import OrdenSerializer, MiOrdenSerializer

import stripe
import json

# Create your views here.


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def pagar(request):
    serializer = OrdenSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        total = sum(item.get('cantidad') * item.get('product').precio for item in serializer.validated_data['items'])

        try:
            cargo = stripe.Charge.create(
                amount = int(total),
                currency = 'MXN',
                description = 'Cargo de MyTech-Ecommerce',
                source = serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, total=total)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListaOrdenes(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        ordenes = Orden.objects.filter(user=request.user)
        serializer = MiOrdenSerializer(ordenes, many=True)
        return Response(serializer.data)


def index(request):
    context = {'segment': 'index'}
    
    print('algo')

    ventas, labels, = Orden.get_reporte_ventas()

    data = [
        {
            'd': dia,
            'm': '{:.2f}'.format(ventas[dia].get('total')),
        } for dia in ventas
    ]

    chart_data = json.dumps({
        'element': 'morris-bar-chart',
        'data': data,
        'xkey': 'd',
        'barSizeRatio': 0.70,
        'barGap': 3,
        'resize': True,
        'responsive': True,
        'ykeys': ['dia', 'monto'],  # it can be custom
        'labels': labels,
        'barColors': ['0-#1de9b6-#1dc4e9', '0-#899FD4-#A389D4', '#04a9f5']  # it can be custom
    })

    return render(request, 'templates/admin/index.html/', {'data': data})


class OrdenesPDFView(View):
    def get(self, request, *args, **kwargs):
        template = get_template('admin/finanzas_ordenes.html')

        ordenes = Orden.objects.all().extra({'fecha': "date(fecha_orden)"}).values()

        totales = Orden.objects.all().aggregate(total_ventas=Sum('total')).get('total_ventas')

        context = {'ordenes': ordenes, 'totales': f'{totales:.2f}'}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf'

        pisaStatus = pisa.CreatePDF(html, dest=response)

        if pisaStatus.err:
            return HttpResponse('Problemas')
        
        return response