# Generated by Django 2.1.3 on 2020-02-02 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotizador', '0012_poliza_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cliente_contact_referencia', to='cotizador.Cliente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cliente_empresa_referencia', to='cotizador.Cliente'),
        ),
    ]
