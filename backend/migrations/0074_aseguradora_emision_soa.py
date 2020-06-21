# Generated by Django 2.1.3 on 2020-06-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0073_auto_20200621_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='aseguradora',
            name='emision_soa',
            field=models.BooleanField(default=False, help_text='Esta aseguradora cobra emisión sobre el valor SOA', verbose_name='Emisión sobre SOA'),
        ),
    ]
