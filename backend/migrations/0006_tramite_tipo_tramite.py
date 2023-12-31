# Generated by Django 2.1.3 on 2020-03-24 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20200324_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='tipo_tramite',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Endoso por póliza'), (2, 'Cancelación de póliza'), (3, 'Cesión de derechos'), (4, 'Corección de póliza'), (5, 'Cotización nueva póliza'), (6, 'Cambio de razón social'), (7, 'Documento de lavado de dinero'), (8, 'Documento de reclamo'), (9, 'Renovaciones'), (10, 'Liquidaciones')], null=True),
        ),
    ]
