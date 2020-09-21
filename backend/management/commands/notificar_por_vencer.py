from django.core.management.base import BaseCommand
from backend.models import *
from django.template.loader import render_to_string
from utils.utils import send_email


class Command(BaseCommand):
    help = 'Autorenovacion automatica de polizas del cotizador'

    def handle(self, *args, **options):
        day = datetime.now() + timedelta(days=30)
        # ps = Poliza.objects.filter(procedencia=ProcedenciaPoliza.COTIZADOR, fecha_emision__isnull=False,
        #                            cliente__isnull=False,
        #                            fecha_vence__year=day.year,
        #                            fecha_vence__month=day.month,
        #                            fecha_vence__day=day.day,
        #                            aseguradora__isnull=False,
        #                            estado_poliza=EstadoPoliza.ACTIVA)
        ps = Poliza.objects.filter(fecha_vence__lte=day)
        for p in ps:
            config = p.get_config()
            if config:
                html = render_to_string('cotizador/email/notificacion_vence.html', {
                    'body': config.email_texto, 'poliza': p
                })
                send_email('Tu póliza # %s está cerca de vencer' % p.no_poliza, config.email_trust, html=html)






