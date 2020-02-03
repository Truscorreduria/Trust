# Generated by Django 2.1.3 on 2020-02-02 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0015_auto_20200202_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='contacto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cliente_contacto_referencia', to='cotizador.Cliente'),
        ),
    ]
