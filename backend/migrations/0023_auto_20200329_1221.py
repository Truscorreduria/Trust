# Generated by Django 2.1.3 on 2020-03-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_auto_20200328_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramite',
            name='estado',
            field=models.CharField(blank=True, choices=[('En Proceso', 'En Proceso'), ('Pendiente documentación', 'Pendiente documentación'), ('Finalizado', 'Finalizado'), ('Anulado', 'Anulado')], default='Pendiente', max_length=55, null=True),
        ),
    ]