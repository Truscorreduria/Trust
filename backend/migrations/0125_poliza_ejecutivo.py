# Generated by Django 2.1.3 on 2020-11-05 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0124_auto_20201105_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='ejecutivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ejecutivo_asignado', to=settings.AUTH_USER_MODEL),
        ),
    ]
