from django import template
from cotizador.models import CoberturaPoliza
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter('valor_cobertura')
def valor_cobertura(poliza, cobertura):
    try:
        return CoberturaPoliza.objects.get(poliza=poliza, cobertura=cobertura).monto
    except ObjectDoesNotExist as e:
        return 0.0

