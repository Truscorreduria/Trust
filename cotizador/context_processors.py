from .models import Entidad, Banner, Departamento, Municipio
from constance import config
from datetime import datetime

def Entidades(request):
    return {'entidades': Entidad.objects.filter(active=True),
            'publicidad': Banner.objects.filter(active=True).order_by('code'),
            'departamentos': Departamento.objects.filter(active=True),
            'municipios': Municipio.objects.filter(active=True),
            'config': config, 'now': datetime.now()}