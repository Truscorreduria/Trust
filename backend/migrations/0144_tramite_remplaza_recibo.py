# Generated by Django 2.1.3 on 2021-04-04 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0143_poliza_recibo_principal'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='remplaza_recibo',
            field=models.BooleanField(default=False, verbose_name='reemplaza recibo principal'),
        ),
    ]