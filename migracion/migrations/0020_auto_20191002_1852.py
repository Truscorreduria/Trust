# Generated by Django 2.1.3 on 2019-10-02 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('migracion', '0019_dependientesepelio_titular'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sepelio',
            options={'ordering': ['asegurado']},
        ),
        migrations.AddField(
            model_name='dependientesepelio',
            name='empleado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='migracion.Empleado'),
        ),
    ]
