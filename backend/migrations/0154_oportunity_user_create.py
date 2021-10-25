# Generated by Django 2.1.3 on 2021-10-20 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0153_auto_20211020_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='oportunity',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backend_oportunity_usuario_crea', to=settings.AUTH_USER_MODEL, verbose_name='usuario que registra'),
        ),
    ]