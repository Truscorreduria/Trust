# Generated by Django 2.1.3 on 2020-10-26 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0117_poliza_perdir_motivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poliza',
            old_name='movivo_cancelacion',
            new_name='motivo_cancelacion',
        ),
    ]