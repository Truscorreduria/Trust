# Generated by Django 2.1.3 on 2021-11-02 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0163_auto_20211102_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistenciatravel',
            name='cliente',
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='am_contacto',
            field=models.CharField(max_length=255, null=True, verbose_name='apellido materno del contacto'),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='ap_contacto',
            field=models.CharField(max_length=255, null=True, verbose_name='apellido paterno del contacto'),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='backend.PlanCategoryTravel'),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='email_contacto',
            field=models.CharField(max_length=255, null=True, verbose_name='email del contacto'),
        ),
        migrations.AddField(
            model_name='asistenciatravel',
            name='nombre_contacto',
            field=models.CharField(max_length=255, null=True, verbose_name='nombre del contacto'),
        ),
    ]
