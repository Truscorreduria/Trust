# Generated by Django 2.1.3 on 2020-03-04 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0058_poliza_total_pagos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pago',
            options={'ordering': ['fecha_vence']},
        ),
    ]
