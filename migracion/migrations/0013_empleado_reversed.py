# Generated by Django 2.1.3 on 2019-09-18 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migracion', '0012_empleado_noblank'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='reversed',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
