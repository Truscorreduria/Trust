# Generated by Django 2.1.3 on 2021-04-04 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0142_poliza_user_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='recibo_principal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recibo_principal', to='backend.Tramite', verbose_name='recibo principal'),
        ),
    ]
