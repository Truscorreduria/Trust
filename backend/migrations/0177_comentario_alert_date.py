# Generated by Django 2.2 on 2022-10-15 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0176_comentario_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='alert_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
