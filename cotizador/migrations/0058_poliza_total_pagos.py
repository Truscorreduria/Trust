# Generated by Django 2.1.3 on 2020-03-04 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0057_pago_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='total_pagos',
            field=models.FloatField(default=0.0),
        ),
    ]