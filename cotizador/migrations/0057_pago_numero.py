# Generated by Django 2.1.3 on 2020-03-04 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0056_auto_20200304_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='numero',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]