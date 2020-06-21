# Generated by Django 2.1.3 on 2020-06-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0068_auto_20200619_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='oportunityquotation',
            name='factor_depreciacion',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='coaseguro_dano',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Coaseguro daño'),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='coaseguro_robo',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Coaseguro robo'),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='deducible',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Mínimo deducible'),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='emision',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Derecha de emision'),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='exceso',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Porcentaje Exceso'),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='suma_asegurada',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Derecha de emision'),
        ),
        migrations.AlterField(
            model_name='oportunityquotation',
            name='tarifa',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Tarifa por millar'),
        ),
    ]