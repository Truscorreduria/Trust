from django.db import models
from grappelli_extras.models import BaseEntity
from image_cropping.fields import ImageCropField
from image_cropping import ImageRatioField


class Departamento(BaseEntity):
    pass


class Municipio(BaseEntity):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="municipios")


class Banner(BaseEntity):
    imagen = ImageCropField(upload_to='banners')
    cropping = ImageRatioField('imagen', '400x800', allow_fullsize=True, verbose_name="vista previa")

    class Meta:
        verbose_name_plural = "Publicidad"