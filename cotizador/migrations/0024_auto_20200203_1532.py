# Generated by Django 2.1.3 on 2020-02-03 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0023_poliza_grupo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobertura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, null=True)),
                ('description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Descripción detallada')),
                ('tipo_calculo', models.PositiveSmallIntegerField(choices=[(1, 'PRECIO FIJO'), (2, 'TASA PORCENTUAL'), (3, 'TASA PORMILLAR')], default=3)),
                ('tipo_cobertura', models.PositiveSmallIntegerField(choices=[(1, 'Básica'), (2, 'Ampliada'), (3, 'Adicional'), (4, 'Opcional')], default=1, verbose_name='variable de cobertura')),
                ('tipo_exceso', models.CharField(choices=[('0.0', '0.0'), ('valor_nuevo', 'Valor de Nuevo'), ('valor_depreciado', 'Valor Depreciado'), ('otro', 'Otro')], default='0.0', max_length=25, verbose_name='variable de calculo')),
                ('iva', models.BooleanField(default=True, verbose_name='aplica iva')),
                ('sub_ramo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coberturas', to='cotizador.SubRamo')),
            ],
            options={
                'verbose_name': 'cobertura',
                'verbose_name_plural': 'coberturas ofrecidas',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='DetalleCobertura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('monto', models.FloatField(default=0.0)),
                ('cobertura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizador.Cobertura')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(default=0.0)),
                ('available', models.BooleanField(default=True)),
                ('aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizador.Aseguradora')),
                ('cobertura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precios', to='cotizador.Cobertura')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='poliza',
            name='nombres',
            field=models.CharField(blank=True, max_length=165, null=True, verbose_name='nombre'),
        ),
    ]