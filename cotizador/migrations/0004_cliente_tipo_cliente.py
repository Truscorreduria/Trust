# Generated by Django 2.1.3 on 2020-01-22 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0003_auto_20200122_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='tipo_cliente',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
