from django.template.loader import get_template
from django import template
from ..models import *

register = template.Library()

@register.simple_tag(name='precio')
def precio(cobertura, aseguradora):
    p, created = Precio.objects.get_or_create(cobertura=cobertura, aseguradora=aseguradora)
    return p