# Generated by Django 2.2 on 2022-10-15 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0177_comentario_alert_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
            ],
            options={
                'ordering': ['-alert_date'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('backend.comentario',),
        ),
    ]
