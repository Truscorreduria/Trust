# Generated by Django 2.1.3 on 2020-03-29 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_auto_20200329_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='CotizadorConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasa_automovil', models.FloatField(default=10.4, verbose_name='Tarifa para el seguro de prima de vehículo')),
                ('soa_automovil', models.FloatField(default=55.0, verbose_name='Tarifa para el seguro obligatorio de vehículo')),
                ('porcentaje_deducible', models.FloatField(default=0.2, verbose_name='Porcentaje deducible global. Puede ir a la seccion de marcas con recargo para cambiar este valor a una marca en específico')),
                ('porcentaje_deducible_extencion_territorial', models.FloatField(default=0.3, verbose_name='Porcentaje deducible solo para la cobertura de extensión territorial. Para aplicar regargo vaya a Marcas con recargo.')),
                ('minimo_deducible', models.FloatField(default=100.0, verbose_name='Mínimo deducible global. Puede ir a la seccion de marcas con recargo para cambiar este valor a una marca en específico')),
                ('soa_descuento', models.FloatField(default=0.05, verbose_name='Descuento del Seguro Obligatorio de Vehículo. Por favor usar notación decimal (0.05 = 5%)')),
                ('email_automovil', models.CharField(default='gcarrion@trustcorreduria.com,', max_length=1000, verbose_name='Lista de correos de automovil usados para las notificaciones del sistema')),
                ('poliza_sepelio', models.CharField(default='CF - 000521 - 0', max_length=65, verbose_name='Número de Póliza para Seguros del Titular.')),
                ('poliza_sepelio_dependiente', models.CharField(default='CF - 000564 - 0', max_length=65, verbose_name='Número de Póliza para Seguros del Dependiente.')),
                ('costo_sepelio', models.FloatField(default=3.75, verbose_name='Costo del Seguro de Sepelio para empleados Banpro.')),
                ('suma_sepelio', models.FloatField(default=1000.0, verbose_name='Suma asegurada para Seguros de Sepelio empleados Banpro.')),
                ('email_sepelio', models.CharField(default='asanchez@segurosamerica.com,', max_length=1000, verbose_name='Lista de correos de sepelio usados para las notificaciones del sistema')),
                ('poliza_accidente', models.CharField(default='APC - 13359 - 30977', max_length=65, verbose_name='Número de Póliza para Seguros de Accidente Banpro.')),
                ('costo_accidente', models.FloatField(default=18.0, verbose_name='Costo del Seguro de Accidentes para empleados Banpro.')),
                ('costo_carnet_accidente', models.FloatField(default=1.85, verbose_name='Costo del carnet para seguros de Accidente')),
                ('suma_accidente', models.FloatField(default=15000.0, verbose_name='Suma asegurada para Seguros de Accidentes del Titular.')),
                ('suma_accidente_dependiente', models.FloatField(default=10000.0, verbose_name='Suma asegurada para Seguros de Accidentes del Dependiente.')),
                ('email_accidente', models.EmailField(default='luis.collado@mapfre.com.ni,', max_length=254, verbose_name='Lista de correos de accidente usados para las notificaciones del sistema')),
                ('poliza_vida', models.CharField(default='CV-000209-0', max_length=65, verbose_name='Número de Póliza para Seguros de Vida Banpro.')),
                ('suma_vida', models.CharField(default='22 veces el salario', max_length=100, verbose_name='Unicamente para la impresión del documento')),
                ('aseguradora_accidente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aseguradora_accidente', to='backend.Aseguradora')),
                ('aseguradora_automovil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aseguradora_automovil', to='backend.Aseguradora')),
                ('aseguradora_sepelio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aseguradora_sepelio', to='backend.Aseguradora')),
                ('aseguradora_vida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aseguradora_vida', to='backend.Aseguradora')),
                ('cliente_accidente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_accidente', to='backend.Cliente', verbose_name='el contratante que se usara en la poliza de sepelio')),
                ('cliente_sepelio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratante_sepelio', to='backend.Cliente', verbose_name='el contratante que se usara en la poliza de sepelio')),
                ('cliente_vida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_vida', to='backend.Cliente', verbose_name='el contratante que se usara en la poliza de sepelio')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ClienteJuridico')),
                ('ramo_accidente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ramo_accidente', to='backend.Ramo')),
                ('ramo_automovil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ramo_automovil', to='backend.Ramo')),
                ('ramo_sepelio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ramo_sepelio', to='backend.Ramo')),
                ('ramo_vida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ramo_vida', to='backend.Ramo')),
                ('sub_ramo_accidente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_ramo_accidente', to='backend.SubRamo')),
                ('sub_ramo_automovil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_ramo_automovil', to='backend.SubRamo')),
                ('sub_ramo_sepelio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_ramo_sepelio', to='backend.SubRamo')),
                ('sub_ramo_vida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_ramo_vida', to='backend.SubRamo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
