# Generated by Django 2.1.3 on 2020-06-16 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0060_oportunity_aseguradora'),
    ]

    operations = [
        migrations.AddField(
            model_name='aseguradora',
            name='coaseguro_dano',
            field=models.FloatField(default=20.0, verbose_name='Coaseguro daño'),
        ),
        migrations.AddField(
            model_name='aseguradora',
            name='coaseguro_robo',
            field=models.FloatField(default=20.0, verbose_name='Coaseguro robo'),
        ),
        migrations.AddField(
            model_name='aseguradora',
            name='deducible',
            field=models.FloatField(default=100.0, verbose_name='Mínimo deducible'),
        ),
        migrations.AddField(
            model_name='aseguradora',
            name='tarifa',
            field=models.FloatField(default=11.0, verbose_name='Tarifa por millar'),
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='exceso',
            field=models.FloatField(default=6.666, verbose_name='Porcentaje Exceso'),
        ),
    ]
