from django import template
from backend.models import CoberturaAseguradora
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter('valor_cobertura')
def valor_cobertura(cobertura, aseguradora):
    return CoberturaAseguradora.objects.get(cobertura_id=cobertura.id, aseguradora_id=aseguradora.id).valor
