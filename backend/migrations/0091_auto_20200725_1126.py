# Generated by Django 2.1.3 on 2020-07-25 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0090_auto_20200725_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='poliza_no',
        ),
    ]
