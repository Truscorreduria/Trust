# Generated by Django 2.1.3 on 2020-08-21 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0104_auto_20200821_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siniestrotramite',
            name='forma_pago',
        ),
    ]
