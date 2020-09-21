from datetime import datetime, timedelta
from utils.utils import send_email
from django.template.loader import render_to_string
from .models import Poliza, EstadoPoliza


def notificaciones_polizas_vencidas():
    day = datetime.now() + timedelta(days=30)
    # ps = Poliza.objects.filter(procedencia=ProcedenciaPoliza.COTIZADOR, fecha_emision__isnull=False,
    #                            cliente__isnull=False,
    #                            fecha_vence__year=day.year,
    #                            fecha_vence__month=day.month,
    #                            fecha_vence__day=day.day,
    #                            aseguradora__isnull=False,
    #                            estado_poliza=EstadoPoliza.ACTIVA)
    ps = Poliza.objects.filter(fecha_vence__lte=day).exclude(estado_poliza=EstadoPoliza.RENOVADA)
    for p in ps:
        html = render_to_string('cotizador/email/notificacion_vence.html', {
            'poliza': p
        })
        send_email('Tu póliza # %s está cerca de vencer' % p.no_poliza,
                   "cesarabel@deltacopiers.com,gcarrion@trustcorreduria.com,sistemas@trustcorreduria.com",
                   html=html)
