# Generated by Django 2.1.3 on 2020-06-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0044_auto_20200606_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='aseguradora',
            name='exceso',
            field=models.FloatField(default=0.0, verbose_name='Porcentaje Exceso'),
        ),
    ]