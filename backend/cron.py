from .signals import *
from django.template import Template, Context


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


def notificacion_por_vencer_grupo():
    """
    Notificacion de pólizas por vencer por grupo.
    """
    inicio = datetime.now()
    fin = inicio + timedelta(days=32)
    for grupo in Grupo.objects.all().order_by('name'):
        html = render_to_string('trustseguros/lte/email/notificacion_por_vencer_grupo.html', {
            'polizas': Poliza.objects.filter(estado_poliza__in=[EstadoPoliza.ACTIVA, EstadoPoliza.PENDIENTE],
                                             grupo=grupo, fecha_vence__gte=inicio, fecha_vence__lte=fin),
            'inicio': inicio, 'fin': fin, 'grupo': grupo
        })
        send_email(f'Recordatorio de Pólizas por Vencer {grupo.name}', grupo.email_notificacion, html=html, files=None)


def notificacion_vencidas_grupo():
    """
    Notificacion de pólizas vencidas por grupo.
    """
    hoy = datetime.now()
    for grupo in Grupo.objects.all().order_by('name'):
        html = render_to_string('trustseguros/lte/email/notificacion_vencidas_grupo.html', {
            'polizas': Poliza.objects.filter(estado_poliza__in=[EstadoPoliza.ACTIVA, EstadoPoliza.PENDIENTE],
                                             grupo=grupo, fecha_vence__lte=hoy),
            'fecha': hoy, 'grupo': grupo
        })
        send_email(f'Recordatorio de Pólizas Vencidas {grupo.name}', grupo.email_notificacion, html=html, files=None)


def notificacion_pagos_por_vencer():
    """
    Notificacion de pagos vencidos
    """
    inicio = datetime.now()
    fin = inicio + timedelta(days=30)
    html = render_to_string('trustseguros/lte/email/notificacion_pagos_por_vencer.html', {
        'pagos': Cuota.objects.filter(estado=EstadoPago.VIGENTE,
                                      fecha_vence__gte=inicio,
                                      fecha_vence__lte=fin),
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
