from django import template
from backend.models import LineaUser
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter('has_line')
def has_line(user, linea):
    try:
        LineaUser.objects.get(linea=linea, user=user)
        return 'checked="checked"'
    except ObjectDoesNotExist:
        return ""
