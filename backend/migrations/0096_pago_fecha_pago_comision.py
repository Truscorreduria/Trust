# Generated by Django 2.1.3 on 2020-07-27 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0095_auto_20200727_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='fecha_pago_comision',
            field=models.DateField(null=True),
        ),
    ]
