# Generated by Django 2.1.3 on 2020-06-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0062_tarifa'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poliza',
            options={'ordering': ['fecha_vence'], 'permissions': (('trust_clientes_natural', 'Clientes Naturales'), ('trust_clientes_juridico', 'Clientes Jurídicos'), ('trust_polizas_poliza', 'Pólizas'), ('trust_polizas_tramite', 'Trámites'), ('trust_catalogos_aseguradora', 'Catálogos Aseguradoras'), ('trust_catalogos_tarifa', 'Catálogos Tarifas'), ('trust_catalogos_linea', 'Línea de negocios'), ('trust_catalogos_campain', 'Campañas'), ('trust_catalogos_grupo', 'Catálogos Grupos'), ('trust_catalogos_ramo', 'Catálogos Ramos'), ('trust_catalogos_subramo', 'Catálogos Sub Ramos'), ('trust_cotizador_empresa', 'Cotizador Empresas Afiliadas'), ('trust_cotizador_marca', 'Cotizador Marcas con Recargo'), ('trust_usuarios_usuario', 'Administrar Usuarios'), ('trust_usuarios_grupo', 'Perfiles y Roles'), ('trust_crm_oportunidad', 'CRM Oportunidades')), 'verbose_name': 'póliza', 'verbose_name_plural': 'Pólizas'},
        ),
        migrations.AddField(
            model_name='oportunity',
            name='rc_exceso',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='oportunity',
            name='valor_exceso',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='oportunity',
            name='valor_nuevo',
            field=models.FloatField(default=0.0),
        ),
    ]
