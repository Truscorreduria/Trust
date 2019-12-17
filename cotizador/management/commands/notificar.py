from django.core.management.base import BaseCommand
from cotizador.models import *
from cotizador.utils import send_email
from django.template.loader import render_to_string
from openpyxl import Workbook
from io import BytesIO


class Command(BaseCommand):
    help = 'Notificacion de debito automatico'

    def handle(self, *args, **options):
        output = BytesIO()
        book = Workbook()
        sheet = book.active
        sheet.append(['# Empl.',
                     'Nombre',
                     'Monto',
                     'Moneda',
                     'Cant. Cuotas a deducir',
                     '# POLIZA',
                     'VIGENCIA'
                      ])
        polizas = Poliza.objects.filter(medio_pago='deduccion_nomina').exclude(
            id__in=Notificacion.objects.filter(poliza__isnull=False).values_list('poliza', flat=True)
        ).exclude(no_poliza='pendiente')
        accidentes = benAccidente.objects.all().exclude(
            id__in=Notificacion.objects.filter(benaccidente__isnull=False).values_list('benaccidente', flat=True))
        sepelios = benSepelio.objects.all().exclude(
            id__in=Notificacion.objects.filter(bensepelio__isnull=False).values_list('bensepelio', flat=True))
        print(polizas, accidentes, sepelios)
        if len(polizas) > 0 or len(accidentes) > 0 or len(sepelios) > 0:
            html = render_to_string('cotizador/email/notificacion_debito.html')
            if len(polizas) > 0:
                for p in polizas:
                    sheet.append([
                        p.user.profile().codigo_empleado,
                        p.nombre_asegurado(),
                        p.total,
                        'DÓLARES',
                        p.cuotas,
                        p.no_poliza,
                        p.fecha_vencimiento()]
                    )

            if len(accidentes) > 0:
                for p in accidentes:
                    sheet.append([
                        p.empleado.codigo_empleado,
                        p.full_name(),
                        p.costo,
                        'DÓLARES',
                        1,
                        p.numero_poliza,
                        p.fecha_vencimiento()]
                    )

            if len(sepelios) > 0:
                for p in sepelios:
                    sheet.append([
                        p.empleado.codigo_empleado,
                        p.full_name(),
                        p.costo,
                        'DÓLARES',
                        1,
                        p.numero_poliza,
                        p.fecha_vencimiento()]
                    )
            book.save(output)

            files = [("attachment", ("Debito planilla.xlsx", output.getvalue())), ]

            send_email('Pendientes débito planilla', config.EMAIL_DEBITO_AUTOMATICO,
                       html=html, files=files)

            if len(polizas) > 0:
                for p in polizas:
                    n = Notificacion(poliza=p, fecha=datetime.now())
                    n.save()

            if len(accidentes) > 0:
                for p in accidentes:
                    n = Notificacion(benaccidente=p, fecha=datetime.now())
                    n.save()

            if len(sepelios) > 0:
                for p in sepelios:
                    n = Notificacion(bensepelio=p, fecha=datetime.now())
                    n.save()





