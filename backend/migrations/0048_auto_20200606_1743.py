# Generated by Django 2.1.3 on 2020-06-06 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0047_auto_20200606_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anno',
            options={'ordering': ['antiguedad'], 'verbose_name': 'año', 'verbose_name_plural': 'Años de antiguedad'},
        ),
    ]