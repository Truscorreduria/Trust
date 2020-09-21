from datetime import datetime, timedelta
from utils.utils import send_email
from .models import Poliza, EstadoPoliza, ProcedenciaPoliza
from django.template import Template, Context


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
            print(content)
            template = Template(content)
            context = Context({
                'poliza': p
            })
            html = template.render(context)
            send_email('Tu póliza # %s está cerca de vencer' % p.no_poliza,
                       "cesarabel@deltacopiers.com,gcarrion@trustcorreduria.com,sistemas@trustcorreduria.com",
                       html=html)
