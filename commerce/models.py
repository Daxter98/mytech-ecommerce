from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File
from django.db import models
from django.db.models import Count
from django.db.models.functions import ExtractDay

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('nombre',)

    
    def __str__(self) -> str:
        return self.nombre

    def get_absolute_url(self):
        return f'/{self.slug}'

class Producto(models.Model): 
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    slug = models.SlugField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='uploads/', blank=True, null=True)
    miniatura = models.ImageField(upload_to='uploads/', blank=True, null=True)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('-fecha_entrada',)

    
    def __str__(self) -> str:
        return self.nombre

    def get_absolute_url(self):
        return f'/{self.categoria.slug}/{self.slug}'

    def get_image(self):
        if self.imagen:
            return 'https://mytech-ecommerce.azurewebsites.net/' + self.imagen.url
        return ''
    
    def get_miniatura(self):
        if self.miniatura:
            return 'https://mytech-ecommerce.azurewebsites.net/' + self.miniatura.url
        else:
            if self.imagen:
                self.miniatura = self.make_thumbnail(self.imagen)
                self.save()

                return 'https://mytech-ecommerce.azurewebsites.net/' + self.miniatura.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    @classmethod
    def get_reporte_inventario(cls):
        inventario = Producto.objects.all().extra({'fecha_ingreso': "date(fecha_entrada)"}).values('fecha_ingreso').annotate(conteo=Count('id'))

            
        data = {}
        for producto in inventario:
            if producto['fecha_ingreso'] not in data:
                data[producto['fecha_ingreso']] = producto['conteo']
            else: 
                data[producto['fecha_ingreso']] += producto['conteo']


        labels = list(data.keys())
        
        return data, labels
