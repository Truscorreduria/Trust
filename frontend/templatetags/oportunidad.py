from django import template
from backend.models import LineaUser, OportunityQuotation
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter('has_line')
def has_line(user, linea):
    try:
        LineaUser.objects.get(linea=linea, user=user)
        return 'checked="checked"'
    except ObjectDoesNotExist:
        return ""


@register.filter('passed')
def passed(choice, status):
    try:
        if int(choice[0]) <= int(status):
            return "on"
        return "off"
    except:
        return "off"


@register.filter('checked')
def checked(company, oportunity):
    try:
        OportunityQuotation.objects.get(aseguradora=company, oportunity=oportunity)
        return 'checked'
    except:
        return ''


@register.filter('suma')
def suma(company, oportunity):
    try:
        return OportunityQuotation.objects.get(aseguradora=company, oportunity=oportunity).suma_asegurada
    except:
        return '-'


@register.filter('deducible')
def deducible(company, oportunity):
    try:
        return OportunityQuotation.objects.get(aseguradora=company, oportunity=oportunity).deducible
    except:
        return '-'


@register.filter('coaseguro_dano')
def coaseguro_dano(company, oportunity):
    try:
        return OportunityQuotation.objects.get(aseguradora=company, oportunity=oportunity).coaseguro_dano
    except:
        return '-'


@register.filter('coaseguro_robo')
def coaseguro_robo(company, oportunity):
    try:
        return OportunityQuotation.objects.get(aseguradora=company, oportunity=oportunity).coaseguro_robo
    except:
        return '-'


@register.filter('prima')
def prima(company, oportunity):
    try:
        return OportunityQuotation.objects.get(aseguradora=company, oportunity=oportunity).prima_total
    except:
        return '-'
