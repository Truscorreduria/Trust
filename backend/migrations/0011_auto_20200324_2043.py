# Generated by Django 2.1.3 on 2020-03-24 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_tramite_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tramite',
            old_name='fecha',
            new_name='fechahora',
        ),
    ]
