from django import template
from backend.models import CoberturaPoliza
from django.core.exceptions import ObjectDoesNotExist
import json

register = template.Library()


@register.filter('valor_cobertura')
def valor_cobertura(poliza, cobertura):
    try:
        return CoberturaPoliza.objects.get(poliza=poliza, cobertura=cobertura).monto
    except ObjectDoesNotExist as e:
        return 0.0


@register.filter('dato_tecnico')
def dato_tecnico(row, field):
    try:
        data = json.loads(row.extra_data)
        return data[field.name]
    except KeyError as e:
        return ""
    except json.decoder.JSONDecodeError as e:
        return ""

