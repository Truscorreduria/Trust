# Generated by Django 2.1.3 on 2020-02-26 22:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0052_auto_20200226_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]