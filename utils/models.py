from django.db import models
from grappelli_extras.models import BaseEntity


class Departamento(BaseEntity):
    pass


class Municipio(BaseEntity):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="municipios")
