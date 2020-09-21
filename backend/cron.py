from datetime import datetime, timedelta
from utils.utils import send_email
from .models import Poliza, EstadoPoliza, ProcedenciaPoliza
from django.template import Template, Context
from frontend.apps.trustseguros.views import iniciar_proc as renovacion_automatica


def notificaciones_polizas_vencidas():
    day = datetime.now() + timedelta(days=30)
    ps = Poliza.objects.filter(procedencia=ProcedenciaPoliza.COTIZADOR, fecha_emision__isnull=False,
                               cliente__isnull=False,
                               fecha_vence__year=day.year,
                               fecha_vence__month=day.month,
                               fecha_vence__day=day.day,
                               aseguradora__isnull=False,
                               estado_poliza=EstadoPoliza.ACTIVA)
    # ps = Poliza.objects.filter(fecha_vence__lte=day).exclude(estado_poliza=EstadoPoliza.RENOVADA)
    print(ps.count())
    for p in ps:
        config = p.get_config()
        if config:
            content = config.email_texto.replace('[[', '{{').replace(']]', '}}')
            template = Template(content)
            context = Context({
                'poliza': p
            })
            destinatario = ""
            # if p.cliente.email_personal:
            #     destinatario += p.cliente.email_personal
            destinatario += config.email_trust
            if p.cesion_derecho:
                destinatario += config.email_cesion_derecho
            html = template.render(context)
            send_email('Tu póliza # %s está cerca de vencer' % p.no_poliza, destinatario,
                       html=html)
