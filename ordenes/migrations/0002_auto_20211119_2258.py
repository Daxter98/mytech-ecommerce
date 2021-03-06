# Generated by Django 3.2.7 on 2021-11-19 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0006_alter_producto_categoria'),
        ('ordenes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticuloOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='orden',
            name='stripe_token',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='ElementoOrden',
        ),
        migrations.AddField(
            model_name='articuloorden',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='ordenes.orden'),
        ),
        migrations.AddField(
            model_name='articuloorden',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='commerce.producto'),
        ),
    ]
