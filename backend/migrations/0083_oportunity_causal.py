# Generated by Django 2.1.3 on 2020-06-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0082_oportunity_aseguradora'),
    ]

    operations = [
        migrations.AddField(
            model_name='oportunity',
            name='causal',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
