# Generated by Django 2.1.3 on 2020-10-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0119_auto_20201026_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='aseguradora',
            name='emision_min',
            field=models.FloatField(default=0.0, verbose_name='monto de emisión mínimo'),
        ),
    ]