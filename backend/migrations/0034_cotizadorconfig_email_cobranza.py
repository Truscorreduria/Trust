# Generated by Django 2.1.3 on 2020-05-06 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_archivo_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizadorconfig',
            name='email_cobranza',
            field=models.CharField(default='gcarrion@trustcorreduria.com,', max_length=1000, null=True, verbose_name='Lista de correos de automovil usados para las notificaciones de cobranza'),
        ),
    ]
