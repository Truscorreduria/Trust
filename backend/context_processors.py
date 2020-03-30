from .models import Entidad
from constance import config
from datetime import datetime


def Entidades(request):
    return {
        'entidades': Entidad.objects.filter(active=True),

        'now': datetime.now()
    }
