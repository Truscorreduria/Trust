# Generated by Django 2.1.3 on 2020-03-24 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20200324_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='aseguradora',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Aseguradora'),
        ),
    ]
