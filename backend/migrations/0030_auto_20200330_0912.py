# Generated by Django 2.1.3 on 2020-03-30 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_fieldmap_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldmap',
            name='destiny_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.CampoAdicional'),
        ),
    ]
