# Generated by Django 2.1.3 on 2020-06-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0050_auto_20200607_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Linea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125, verbose_name='nombre de la línea')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
