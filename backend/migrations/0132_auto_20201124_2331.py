# Generated by Django 2.1.3 on 2020-11-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0131_auto_20201124_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='linea',
            name='calcular_cotizacion',
            field=models.BooleanField(default=True, verbose_name='calcular cotizacion por aseguradora'),
        ),
        migrations.AddField(
            model_name='linea',
            name='calcular_valor_nuevo',
            field=models.BooleanField(default=True, verbose_name='calcular valor de nuevo'),
        ),
        migrations.AddField(
            model_name='linea',
            name='contenido_correo',
            field=models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Contenido del correo'),
        ),
        migrations.AddField(
            model_name='linea',
            name='formato_cotizacion',
            field=models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Formato de la cotizacion'),
        ),
    ]
