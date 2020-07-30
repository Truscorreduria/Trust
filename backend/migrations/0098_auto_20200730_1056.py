# Generated by Django 2.1.3 on 2020-07-30 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0097_auto_20200730_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='modificando_recibo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='poliza',
            name='recibo_editar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recibo_a_editar', to='backend.Tramite', verbose_name='recibo a editar'),
        ),
    ]
