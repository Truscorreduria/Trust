# Generated by Django 2.1.3 on 2020-05-06 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0032_auto_20200401_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='tag',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]