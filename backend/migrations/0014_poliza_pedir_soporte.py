# Generated by Django 2.1.3 on 2020-03-25 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20200325_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='pedir_soporte',
            field=models.BooleanField(default=False),
        ),
    ]