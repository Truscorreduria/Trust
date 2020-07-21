# Generated by Django 2.1.3 on 2020-07-21 08:57

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0088_poliza_oportunity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizadorconfig',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('imagen', '400x800', adapt_rotation=False, allow_fullsize=True, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='vista previa'),
        ),
        migrations.AddField(
            model_name='cotizadorconfig',
            name='imagen',
            field=image_cropping.fields.ImageCropField(blank=True, null=True, upload_to='banners'),
        ),
    ]
