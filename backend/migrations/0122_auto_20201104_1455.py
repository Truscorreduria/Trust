# Generated by Django 2.1.3 on 2020-11-04 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0121_aseguradora_monto_soa'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='amount_comision_eje',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='total comisión ejecutivo'),
        ),
        migrations.AddField(
            model_name='poliza',
            name='per_comision_eje',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='% comisión ejecutivo'),
        ),
    ]
