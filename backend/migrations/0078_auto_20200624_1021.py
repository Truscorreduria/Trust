# Generated by Django 2.1.3 on 2020-06-24 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0077_oportunity_fecha_vence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oportunityquotation',
            name='oportunity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to='backend.Oportunity'),
        ),
    ]