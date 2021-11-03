# Generated by Django 2.1.3 on 2021-11-02 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0165_auto_20211102_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistenciatravel',
            name='pais_destino',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pais_destino', to='backend.CountryTravel'),
        ),
        migrations.AlterField(
            model_name='asistenciatravel',
            name='pais_origen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pais_origen', to='backend.CountryTravel'),
        ),
    ]
