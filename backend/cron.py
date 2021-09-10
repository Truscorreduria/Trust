from .signals import *
from django.template import Template, Context
from io import BytesIO
from openpyxl import Workbook
from twilio.rest import Client
from django.conf import settings

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)


def notificaciones_polizas_vencidas():
    """
    Notificacion de pólizas vencidas hacia los clientes
    """
    day = datetime.now() + timedelta(days=30)
    ps = Poliza.objects.filter(procedencia=ProcedenciaPoliza.COTIZADOR, fecha_emision__isnull=False,
                               cliente__isnull=False,
                               fecha_vence__year=day.year,
                               fecha_vence__month=day.month,
                               fecha_vence__day=day.day,
                               aseguradora__isnull=False,
                               estado_poliza=EstadoPoliza.ACTIVA)
    for p in ps:
        config = p.get_config()
        if config:
            content = config.email_texto.replace('[[', '{{').replace(']]', '}}')
            template = Template(content)
            context = Context({
                'poliza': p
            })
            destinatario = ""
            destinatario += config.email_trust
            if p.cesion_derecho:
                destinatario += config.email_cesion_derecho
            html = template.render(context)
            send_email('Tu póliza # %s está cerca de vencer' % p.no_poliza, destinatario,
                       html=html)


def renovacion_automatica():
    ps = Poliza.objects.filter(procedencia=ProcedenciaPoliza.COTIZADOR, fecha_emision__isnull=False,
                               aseguradora__isnull=False,
                               estado_poliza__in=[EstadoPoliza.ACTIVA, EstadoPoliza.PENDIENTE],
                               cliente__isnull=False, fecha_vence__lte=datetime.now(),
                               grupo__in=Grupo.objects.filter(autorenovacion=True))
    for p in ps:
        nueva = RenovarPoliza.send(p)[0][1]
        nueva.user = p.user
        nueva.suma_asegurada = p.aseguradora.depreciar(p.valor_nuevo, p.anno)
        nueva.marca = p.marca
        nueva.modelo = p.modelo
        nueva.chasis = p.chasis
        nueva.anno = p.anno
        nueva.placa = p.placa
        nueva.color = p.color
        nueva.circulacion = p.circulacion
        nueva.tipo_cobertura = p.tipo_cobertura
        nueva.porcentaje_deducible = p.porcentaje_deducible
        nueva.porcentaje_deducible_extension = p.porcentaje_deducible_extension
        nueva.minimo_deducible = p.minimo_deducible
        nueva.minimo_deducible_extension = p.minimo_deducible_extension
        nueva.moneda = p.moneda
        nueva.costo_exceso = p.costo_exceso
        nueva.monto_exceso = p.monto_exceso
        nueva.valor_nuevo = p.valor_nuevo
        nueva.subtotal = p.subtotal
        nueva.descuento = p.descuento
        nueva.emision = p.emision
        nueva.iva = p.iva
        nueva.otros = p.otros
        nueva.total = p.total
        nueva.per_comision = p.per_comision
        nueva.amount_comision = p.amount_comision
        nueva.cesion_derecho = p.cesion_derecho
        nueva.beneficiario = p.beneficiario
        nueva.cesioinario = p.cesioinario
        nueva.forma_pago = p.forma_pago
        nueva.f_pago = p.f_pago
        nueva.medio_pago = p.medio_pago
        nueva.m_pago = p.m_pago
        nueva.cuotas = p.cuotas
        nueva.moneda_cobro = p.moneda_cobro
        nueva.banco_emisor = p.banco_emisor
        nueva.file_circulacion = p.file_circulacion
        nueva.save()


def notificacion_pagos_por_vencer():
    """
    Notificacion de pagos vencidos
    """
    inicio = datetime.now()
    fin = inicio + timedelta(days=30)
    cuotas = Cuota.objects.filter(estado=EstadoPago.VIGENTE,
                                  fecha_vence__gte=inicio,
                                  fecha_vence__lte=fin)
    html = render_to_string('trustseguros/lte/email/notificacion_pagos_por_vencer.html', {
        'pagos': cuotas,
        'inicio': inicio,
        'fin': fin,
    })
    send_email(f'Recordatorio de pagos pendientes {inicio.strftime("%d/%m/%Y")}',
               'sistemas@trustcorreduria.com',
               html=html,
               files=None)


def notificacion_pagos_vencidos():
    """
    Notificacion de pagos vencidos
    """
    hoy = datetime.now()
    pagos = Cuota.objects.filter(estado=EstadoPago.VIGENTE,
                                 fecha_vence__lte=hoy)
    html = render_to_string('trustseguros/lte/email/notificacion_pagos_vencidos.html', {
        'pagos': Poliza.objects.filter(id__in=pagos.values_list('poliza_id', flat=True)).order_by('fecha_vence'),
        'fecha': hoy,
    })
    send_email(f'Recordatorio de pagos vencidos {hoy.strftime("%d/%m/%Y")}',
               'sistemas@trustcorreduria.com',
               html=html,
               files=None)


def notificar_polizas_por_vencer(fecha):
    grupos = Grupo.objects.all()
    for grupo in grupos:
        polizas = Poliza.objects.filter(grupo=grupo,
                                        fecha_vence__year=fecha.year,
                                        fecha_vence__month=fecha.month,
                                        fecha_vence__day=fecha.day,
                                        estado_poliza__in=[EstadoPoliza.ACTIVA, EstadoPoliza.PENDIENTE]
                                        )
        if polizas and polizas.count() > 0:
            html = render_to_string('trustseguros/lte/email/notificacion_por_vencer_grupo.html', {
                'grupo': grupo,
                'polizas': polizas,
            })
            attachment = BytesIO()
            book = Workbook()
            sheet = book.active
            sheet.append([
                'Número de Póliza',
                'Cliente',
                'Fecha de vencimiento',
                'Grupo',
                'Ejecutivo',
            ])
            for poliza in polizas:
                sheet.append([
                    poliza.no_poliza,
                    poliza.cliente.get_full_name(),
                    poliza.fecha_vence.strftime('%d/%m/%y'),
                    poliza.grupo.name,
                    poliza.ejecutivo.get_full_name(),
                ])
            book.save(attachment)
            subject = f'Recordatorio de Pólizas por Vencer {grupo.name} {fecha.strftime("%d/%m/%y")}'
            files = [("attachment", ('Polizas por vencer.xlsx', attachment.getvalue(), 'application/vnd.ms-excel')), ]
            send_email(subject,
                       grupo.email_notificacion,
                       html=html,
                       files=files
                       )


def polizas_por_vencer_30():
    hoy = datetime.now()
    fecha = hoy + timedelta(days=30)
    notificar_polizas_por_vencer(fecha)


def polizas_por_vencer_60():
    hoy = datetime.now()
    fecha = hoy + timedelta(days=60)
    notificar_polizas_por_vencer(fecha)


def notificar_poliza_por_vencer_cliente_email(poliza, email):
    email = "sistemas@trustcorreduria.com,xangcastle@gmail.com"
    grupo = poliza.grupo
    content = grupo.email_cliente.replace('[[', '{{').replace(']]', '}}')
    template = Template(content)
    context = Context({
        'poliza': poliza
    })
    html = template.render(context)
    send_email('Tu póliza # %s está cerca de vencer' % poliza.no_poliza, email,
               html=html)


def notificar_poliza_por_vencer_cliente_sms(poliza, numero):
    numero = "+50583545689"
    message = client.messages.create(
        body=f'Tu póliza # {poliza.no_poliza} está cerca de vencer',
        from_='+15017122661',
        to=numero
    )
    return message.sid


def polizas_por_vencer_cliente():
    now = datetime.now()
    fecha = now + timedelta(days=32)
    polizas = Poliza.objects.filter(estado_poliza=EstadoPoliza.ACTIVA,
                                    fecha_vence__day=fecha.day,
                                    fecha_vence__month=fecha.month,
                                    fecha_vence__year=fecha.year,
                                    )
    if polizas and polizas.count() > 0:
        for poliza in polizas:
            cliente = poliza.cliente
            if cliente.tipo_cliente == TipoCliente.NATURAL and cliente.email_personal:
                notificar_poliza_por_vencer_cliente_email(poliza, cliente.email_personal)
                if cliente.celular:
                    pass
                    # notificar_poliza_por_vencer_cliente_sms(poliza, cliente.celular)
            if cliente.tipo_cliente == TipoCliente.JURIDICO:
                contactos = Contacto.objects.filter(cliente=cliente)
                if contactos and contactos.count() > 0:
                    if contactos[0].email:
                        notificar_poliza_por_vencer_cliente_email(poliza, contactos[0].email)
                    if contactos[0].celular:
                        pass
                        # notificar_poliza_por_vencer_cliente_sms(poliza, contactos[0].celular)


def polizas_vencidas():
    now = datetime.now()
    grupos = Grupo.objects.all()
    for grupo in grupos:
        polizas = Poliza.objects.filter(grupo=grupo,
                                        fecha_vence__year=now.year,
                                        fecha_vence__month=now.month,
                                        fecha_vence__day=now.day,
                                        estado_poliza__in=[EstadoPoliza.ACTIVA, EstadoPoliza.PENDIENTE]
                                        )
        if polizas and polizas.count() > 0:
            attachment = BytesIO()
            book = Workbook()
            sheet = book.active
            sheet.append([
                'Número de Póliza',
                'Cliente',
                'Fecha de vencimiento',
                'Grupo',
                'Ejecutivo',
            ])
            for poliza in polizas:
                sheet.append([
                    poliza.no_poliza,
                    poliza.cliente.get_full_name(),
                    poliza.fecha_vence.strftime('%d/%m/%y'),
                    poliza.grupo.name,
                    poliza.ejecutivo.get_full_name(),
                ])
            book.save(attachment)
            files = [("attachment", ('Polizas por vencer.xlsx', attachment.getvalue(), 'application/vnd.ms-excel')), ]
            send_email(f'Pólizas vencidas al día de hoy {now.strftime("%d/%m/%Y")} {grupo.name}',
                       receipt='sistemas@trustcorreduria.com',
                       html=f'Cantidad de pólizas vencidas {polizas.count()}',
                       files=files)
