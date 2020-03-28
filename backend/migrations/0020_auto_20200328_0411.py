# Generated by Django 2.1.3 on 2020-03-28 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_auto_20200326_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='amount_comision',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='total comisión'),
        ),
        migrations.AddField(
            model_name='tramite',
            name='cuotas',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='tramite',
            name='descuento',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='tramite',
            name='f_pago',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Contado'), (2, 'Fraccionado')], null=True, verbose_name='forma de pago'),
        ),
        migrations.AddField(
            model_name='tramite',
            name='fecha_pago',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tramite',
            name='m_pago',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Transferencia'), (2, 'Cheques'), (3, 'Depositos'), (6, 'Tarjeta de Credito')], null=True, verbose_name='medio de pago'),
        ),
        migrations.AddField(
            model_name='tramite',
            name='moneda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Moneda'),
        ),
        migrations.AddField(
            model_name='tramite',
            name='otros',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='tramite',
            name='per_comision',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='% comisión'),
        ),
        migrations.AlterField(
            model_name='tramite',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticketes', to=settings.AUTH_USER_MODEL, verbose_name='ingresado por'),
        ),
    ]
