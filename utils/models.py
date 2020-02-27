from django.db import models
from grappelli_extras.models import BaseEntity, base
from image_cropping.fields import ImageCropField
from image_cropping import ImageRatioField


class Departamento(BaseEntity):
    pass


class Municipio(BaseEntity):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="municipios")

    def __str__(self):
        return self.name


class Direccion(base):
    departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="%(class)s_departamento")
    municipio = models.ForeignKey(Municipio, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name="%(class)s_municipio")
    domicilio = models.TextField(max_length=400, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True, verbose_name="teléfono")

    class Meta:
        abstract = True


class Banner(BaseEntity):
    imagen = ImageCropField(upload_to='banners')
    cropping = ImageRatioField('imagen', '400x800', allow_fullsize=True, verbose_name="vista previa")

    class Meta:
        verbose_name_plural = "Publicidad"

    def __str__(self):
        return self.name
