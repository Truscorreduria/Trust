# Generated by Django 2.1.3 on 2020-08-27 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0101_auto_20200827_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuota',
            name='fecha_pago',
        ),
        migrations.AddField(
            model_name='pagocuota',
            name='fecha_pago',
            field=models.DateField(null=True),
        ),
    ]
