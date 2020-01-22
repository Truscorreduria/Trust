# Generated by Django 2.1.3 on 2020-01-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0009_auto_20200122_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteProspecto',
            fields=[
            ],
            options={
                'verbose_name': 'prospecto',
                'proxy': True,
                'indexes': [],
            },
            bases=('cotizador.cliente',),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado_cliente',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Prospecto'), (2, 'Cliente activo'), (3, 'Cliente inactivo')], default=2, null=True),
        ),
    ]
