from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from commerce.views import AlmacenPDFView

from ordenes.views import OrdenesPDFView

admin.site.site_url = 'https://polite-sand-0e67d3410.azurestaticapps.net/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('commerce.urls')),
    path('api/v1/', include('ordenes.urls')),
    path('reporte/ventas/', AlmacenPDFView.as_view(), name='reporte_productos'),
    path('reporte/finanzas/ordenes/', OrdenesPDFView.as_view(), name='reporte_ordenes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
