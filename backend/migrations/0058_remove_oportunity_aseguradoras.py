# Generated by Django 2.1.3 on 2020-06-15 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0057_auto_20200614_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oportunity',
            name='aseguradoras',
        ),
    ]