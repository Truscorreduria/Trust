# Generated by Django 2.1.3 on 2021-02-23 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0141_auto_20210223_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='user_create',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='usuario que registra'),
        ),
    ]
