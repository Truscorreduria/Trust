# Generated by Django 2.1.3 on 2020-06-19 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0066_auto_20200619_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='oportunity',
            name='extra_data',
            field=models.CharField(blank=True, max_length=1000000, null=True, verbose_name='datos técnicos'),
        ),
    ]
