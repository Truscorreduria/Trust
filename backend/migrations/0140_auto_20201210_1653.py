# Generated by Django 2.1.3 on 2020-12-10 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0139_auto_20201210_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='campain',
            name='anno',
            field=models.PositiveIntegerField(default=2020, verbose_name='año base'),
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='calc_alt',
            field=models.BooleanField(default=False, help_text='Al activar esta opción se usa un método de calculo ligeramente diferente, detallado en la documentación', verbose_name='Método de calculo alternativo'),
        ),
    ]