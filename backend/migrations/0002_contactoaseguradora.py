# Generated by Django 2.1.3 on 2020-03-24 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactoAseguradora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=355)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]