# Generated by Django 3.2.7 on 2021-11-07 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_productos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('miniatura', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto', to='commerce.categoria')),
            ],
            options={
                'ordering': ('-fecha_entrada',),
            },
        ),
        migrations.DeleteModel(
            name='Productos',
        ),
    ]
