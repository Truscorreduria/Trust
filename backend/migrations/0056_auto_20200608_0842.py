# Generated by Django 2.1.3 on 2020-06-08 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0055_auto_20200607_1758'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oportunity',
            options={'verbose_name': 'oportunidad', 'verbose_name_plural': 'oportunidades'},
        ),
        migrations.AddField(
            model_name='oportunity',
            name='campain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Campain', verbose_name='campaña'),
        ),
    ]
