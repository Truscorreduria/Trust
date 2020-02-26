# Generated by Django 2.1.3 on 2020-02-25 23:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cotizador', '0047_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 2, 25, 23, 28, 31, 906619)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='archivo',
            name='created_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivo_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='archivo',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='archivo',
            name='updated_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='archivo_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='poliza',
            name='no_recibo',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='número de recibo'),
        ),
    ]
