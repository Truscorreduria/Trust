# Generated by Django 2.1.3 on 2020-06-25 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0079_coberturaaseguradora'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coberturaaseguradora',
            unique_together={('cobertura', 'aseguradora')},
        ),
    ]