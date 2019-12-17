from .models import Banner, Departamento, Municipio


def Utils(request):
    return {
        'departamentos': Departamento.objects.filter(active=True),
        'municipios': Municipio.objects.filter(active=True),
        'publicidad': Banner.objects.filter(active=True).order_by('code'),
    }
