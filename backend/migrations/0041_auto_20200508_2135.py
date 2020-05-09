# Generated by Django 2.1.3 on 2020-05-08 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0040_solicitudrenovacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudrenovacion',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='solicitudrenovacion',
            name='poliza',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Poliza'),
        ),
        migrations.AddField(
            model_name='solicitudrenovacion',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
