# Generated by Django 2.1.3 on 2020-05-06 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0037_auto_20200506_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizadorconfig',
            name='email_texto',
            field=models.TextField(default='', max_length=10000, null=True, verbose_name='Contenido del correo'),
        ),
    ]
