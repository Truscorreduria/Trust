# Generated by Django 2.1.3 on 2020-02-25 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0043_auto_20200225_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datopoliza',
            name='extra_data',
            field=models.CharField(blank=True, max_length=1000000, null=True, verbose_name='datos técnicos'),
        ),
    ]
