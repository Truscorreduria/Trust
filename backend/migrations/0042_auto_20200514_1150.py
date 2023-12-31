# Generated by Django 2.1.3 on 2020-05-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0041_auto_20200508_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='benaccidente',
            name='cuotas',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='benaccidente',
            name='monto_cuota',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='bensepelio',
            name='cuotas',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='bensepelio',
            name='monto_cuota',
            field=models.FloatField(default=0.0),
        ),
    ]
