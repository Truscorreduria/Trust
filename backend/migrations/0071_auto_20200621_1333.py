# Generated by Django 2.1.3 on 2020-06-21 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0070_auto_20200621_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oportunityquotation',
            name='monto_exceso',
        ),
        migrations.RemoveField(
            model_name='oportunityquotation',
            name='valor_exceso',
        ),
    ]