# Generated by Django 3.2.7 on 2021-11-20 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0003_orden_codigo_postal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articuloorden',
            old_name='producto',
            new_name='product',
        ),
    ]
