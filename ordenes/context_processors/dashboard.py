from ordenes.models import Orden
from commerce.models import Producto
from django.contrib.auth.models import User
import json

def dashboard(request):
    ventas, labelsVentas = Orden.get_reporte_ventas()

    productos, labelsProductos = Producto.get_reporte_inventario()

    usuarios = [user for user in User.objects.values()]
    
    datosVentas = [float(total) for total in ventas.values()]

    datosProductos = [i for i in productos.values()]

    chart_data = json.dumps({
        'type': 'line',
        'responsive': True,
        'data': {
            'labels': labelsVentas,
            'datasets': [{
                'label': 'Ventas',
                'data': datosVentas,
                'backgroundColor': [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            'fill': False,
            'borderWidth': 2,
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)' 
            ],
            'borderWidth': 1
            }]
        },
        'options': {
            'maintainAspectRatio': False,
            'responsive': True,
            'scales': {
                'yAxes': [{

                'gridLines': {
                    'drawBorder': True,
                    'color': 'rgba(29,140,248,0.1)',
                    'zeroLineColor': "transparent",
                },
                'ticks': {
                    'suggestedMin': 60,
                    'suggestedMax': 120,
                    'padding': 20,
                    'fontColor': "#9e9e9e"
                }
                }],

                'xAxes': [{

                'gridLines': {
                    'drawBorder': False,
                    'color': 'rgba(29,140,248,0.1)',
                    'zeroLineColor': "transparent",
                },
                'ticks': {
                    'padding': 20,
                    'fontColor': "#9e9e9e"
                }
                }]
            }
        }
    })

    product_chart_data = json.dumps({
        'type': 'bar',
        'responsive': True,
        'data': {
            'labels': labelsProductos,
            'datasets': [{
                'label': 'Productos Ingresados',
                'data': datosProductos,
                'backgroundColor': [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            'fill': False,
            'borderWidth': 2,
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)' 
            ]
            }]
        },
        'options': {
            'maintainAspectRatio': False,
            'responsive': True,
            'scales': {
                'yAxes': [{

                'gridLines': {
                    'drawBorder': True,
                    'color': 'rgba(29,140,248,0.1)',
                    'zeroLineColor': "transparent",
                },
                'ticks': {
                    'suggestedMin': 1,
                    'suggestedMax': 10,
                    'padding': 20,
                    'fontColor': "#9e9e9e"
                }
                }],

                'xAxes': [{

                'gridLines': {
                    'drawBorder': False,
                    'color': 'rgba(29,140,248,0.1)',
                    'zeroLineColor': "transparent",
                },
                'ticks': {
                    'padding': 20,
                    'fontColor': "#9e9e9e"
                }
                }]
            }
        }
    })


    return {'ventas': chart_data, 'usuarios': usuarios, 'almacen': product_chart_data}