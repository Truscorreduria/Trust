# Generated by Django 2.1.3 on 2021-11-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0159_auto_20211102_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistenciatravel',
            name='codigo',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='documento',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='referencia',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='ruta',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='valor',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
