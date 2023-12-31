# Generated by Django 2.1.3 on 2020-06-25 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0078_auto_20200624_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoberturaAseguradora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=150)),
                ('aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Aseguradora')),
                ('cobertura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Cobertura')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
