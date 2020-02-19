# Generated by Django 2.1.3 on 2020-02-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0037_auto_20200219_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='tipo_identificacion',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Cédula'), (2, 'Pasaporte'), (3, 'Cédula de residente'), (4, 'Otro')], default=1, null=True),
        ),
    ]
