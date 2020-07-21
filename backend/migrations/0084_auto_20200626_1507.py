# Generated by Django 2.1.3 on 2020-06-26 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0083_oportunity_causal'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobertura',
            name='en_cotizacion',
            field=models.BooleanField(default=False, verbose_name='en la cotización'),
        ),
        migrations.AlterField(
            model_name='oportunity',
            name='causal',
            field=models.CharField(blank=True, choices=[('A', 'Teléfono Apagado.'), ('B', 'Crédito Cancelado'), ('C', 'Es empleado BANPRO'), ('D', 'Número de Teléfono Equivocado.'), ('E', 'Teléfono fuera de Área / Cobertura.'), ('F', 'Fuera del país.'), ('G', 'No Contesta Teléfono.'), ('H', 'No hay información.'), ('I', 'Presentará Externa Cartera Directa.'), ('J', ' Presentará Externa Corredor.'), ('K', 'Seguro Comparativo.'), ('L', 'Ilocalizable.'), ('M', 'VIP')], max_length=1, null=True),
        ),
    ]