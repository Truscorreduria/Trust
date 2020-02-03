from django.template.loader import get_template
from django import template
from ..models import *

register = template.Library()

@register.simple_tag(name='precio')
def comparativo_depreciacion(cobertura, cotizacion):
    pass