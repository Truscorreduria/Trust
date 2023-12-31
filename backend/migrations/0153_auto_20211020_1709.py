# Generated by Django 2.1.3 on 2021-10-20 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0152_auto_20211020_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backend_cliente_usuario_crea', to=settings.AUTH_USER_MODEL, verbose_name='usuario que registra'),
        ),
        migrations.AddField(
            model_name='prospect',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backend_prospect_usuario_crea', to=settings.AUTH_USER_MODEL, verbose_name='usuario que registra'),
        ),
    ]
