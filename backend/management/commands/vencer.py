from django.core.management.base import BaseCommand
from backend.models import *
from utils.utils import send_email
from django.template.loader import render_to_string
from openpyxl import Workbook
from io import BytesIO
from constance import config


class Command(BaseCommand):
    help = 'Notificacion polizas a vencer'

    def handle(self, *args, **options):
        print("comenzando envio...")
        today = datetime.now()
        print("fecha --> ", today.strftime('%d%m%Y'))
        sixtydays = today + timedelta(days=60)
        output = BytesIO()
        book = Workbook()
        sheet = book.active
        sheet.append(['Número de póliza',
                     'Cliente',
                     'Aseguradora',
                     'Moneda',
                     'Ramo',
                     'Sub ramo',
                     'Grupo'
                      ])
        polizas = Poliza.objects.filter(estado_poliza=EstadoPoliza.ACTIVA, fecha_vence__lte=sixtydays)
        print("polizas: ", str(polizas.count()))
        html = render_to_string('cotizador/email/notificacion_vence.html')
        if len(polizas) > 0:
            for p in polizas:
                sheet.append([
                    p.no_poliza,
                    p.cliente.nombre,
                    p.aseguradora.name,
                    p.moneda.moneda,
                    p.ramo.name,
                    p.sub_ramo.name,
                    p.grupo.name]
                )

        book.save(output)

        files = [("attachment", ("Polizas a vencer %s.xlsx" % today.strftime('%d%m%Y'), output.getvalue())), ]

        send_email('Polizas a vencer %s' % today.strftime('%d%m%Y'), config.EMAIL_TRUST,
                   html=html, files=files)
        print("correo enviado con éxito")





