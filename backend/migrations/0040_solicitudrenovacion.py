# Generated by Django 2.1.3 on 2020-05-08 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0039_auto_20200508_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudRenovacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_pago', models.CharField(blank=True, default='anual', max_length=25, null=True)),
                ('f_pago', models.PositiveIntegerField(blank=True, choices=[(1, 'Contado'), (2, 'Fraccionado')], null=True, verbose_name='forma de pago')),
                ('medio_pago', models.CharField(blank=True, choices=[('debito_automatico', 'Débito automático'), ('deduccion_nomina', 'Deducción de nómina'), ('deposito_referenciado', 'Depósito referenciado')], max_length=25, null=True)),
                ('m_pago', models.PositiveIntegerField(blank=True, choices=[(1, 'Transferencia'), (2, 'Cheques'), (3, 'Depositos'), (6, 'Tarjeta de Credito')], null=True, verbose_name='medio de pago')),
                ('cuotas', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('monto_cuota', models.FloatField(blank=True, default=0.0, null=True)),
                ('moneda_cobro', models.CharField(blank=True, max_length=3, null=True)),
                ('banco_emisor', models.CharField(blank=True, max_length=25, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
