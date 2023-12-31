from django.dispatch import Signal
from .models import *
from django.template.loader import render_to_string
from utils.utils import send_email
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from easy_pdf.rendering import render_to_pdf
import os


def get_extension(file):
    name, ext = os.path.splitext(file.name)
    return ext


def add_log(sender, **kwargs):
    request = kwargs.get('request')
    ct = ContentType.objects.get_for_model(sender.__class__)

    message = "El usuario ha aceptado los términos y condiciones y autorizó el manejo de datos y envío por correo electrónico."

    if request.user_agent.is_mobile:
        message += "Tipo de dispositivo: Teléfono. "
    if request.user_agent.is_tablet:
        message += "Tipo de dispositivo: Tablet. "
    if request.user_agent.is_pc:
        message += "Tipo de dispositivo: PC. "
    if request.user_agent.is_bot:
        message += "Tipo de dispositivo: BOT. "

    message += "Navegador: %s, %s " % (request.user_agent.browser.family,
                                       request.user_agent.browser.version_string)

    message += "Sistema Operativo: %s, %s " % (request.user_agent.os.family,
                                               request.user_agent.os.version_string)

    message += "Familia de Dispositivos: " + request.user_agent.device.family

    message += " IP público: " + request.META['REMOTE_ADDR']

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ct.pk,
        object_id=sender.pk,
        object_repr=str(sender),
        action_flag=ADDITION,
        change_message=message)


def notificar_nueva_poliza(sender, **kwargs):
    request = kwargs.get('request', None)
    config = get_config(sender.user)

    files = []
    try:
        for n, f in enumerate(request.FILES.getlist('file_cedula')):
            file = Archivo.add_file(sender, f, 'cedula', tag='cedula', request=request)
            files.append(("attachment", ("Cedula %s" % n + get_extension(file.archivo), file.archivo.read())))
        sender.file_cedula = request.FILES['file_cedula']

    except:
        pass
    try:
        for n, f in enumerate(request.FILES.getlist('file_circulacion')):
            file = Archivo.add_file(sender, f, 'circulacion', tag='circulacion', request=request)
            files.append(("attachment", ("Circulacion %s" % n + get_extension(file.archivo), file.archivo.read())))
        sender.file_circulacion = request.FILES['file_circulacion']
    except:
        pass
    try:
        sender.file_carta = request.FILES['file_carta']
        files.append(("attachment", ("Compra Venta" + get_extension(sender.file_carta),
                                     sender.file_carta.read())))
        Archivo.add_file(sender, sender.file_carta, 'compraventa', tag='compraventa', request=request)
    except:
        pass

    html = render_to_string('cotizador/email/notificacion_automovil.html',
                            context={'object': sender, 'opts': sender._meta},
                            request=request)

    if sender.forma_pago == 'mensual' and sender.medio_pago == 'deduccion_nomina':
        deduccion = render_to_pdf('cotizador/pdf/deduccion.html', {
            'poliza': sender
        })
        files.append(("attachment", ("Consentimiento.pdf", deduccion)))

    ot = render_to_pdf('cotizador/pdf/orden_trabajo.html', {
        'poliza': sender, 'soa_descontado': round((config.soa_automovil * (1 - config.soa_descuento)), 2),
        'config': config
    })

    esquela = render_to_pdf('cotizador/pdf/esquela.html', {
        'poliza': sender
    })

    files.append(("attachment", ("Orden de Trabajo.pdf", ot)))
    files.append(("attachment", ("Esquela.pdf", esquela)))

    send_email('Nueva solicitud - %s' % sender.cliente.get_full_name(), config.email_trust + config.email_automovil,
               html=html, files=files)


def notificar_debito_automatico(sender, **kwargs):
    config = get_config(sender.user)
    if sender.medio_pago == 'debito_automatico':
        request = kwargs.get('request', None)
        html = render_to_string('cotizador/email/notificacion_automovil.html',
                                context={'object': sender, 'opts': sender._meta},
                                request=request)
        ot = render_to_pdf('cotizador/pdf/orden_trabajo.html', {
            'poliza': sender
        })

        esquela = render_to_pdf('cotizador/pdf/esquela.html', {
            'poliza': sender
        })
        files = list()
        files.append(("attachment", ("Orden de Trabajo.pdf", ot)))
        files.append(("attachment", ("Esquela.pdf", esquela)))

        send_email('Nueva solicitud con débito automático', config.email_cobranza,
                   html=html, files=files)


nueva_poliza = Signal()
nueva_poliza.connect(add_log)
nueva_poliza.connect(notificar_nueva_poliza)
nueva_poliza.connect(notificar_debito_automatico)


def notificar_poliza_lista(sender, **kwargs):
    request = kwargs.get('request')
    html = render_to_string('cotizador/email/notificacion_poliza.html',
                            context={'object': sender, 'opts': sender._meta},
                            request=request)

    send_email('Nueva solicitud de poliza de automovil', sender.user.email,
               html=html)
    sender.notificado = True
    sender.save()
    messages.add_message(request, messages.INFO,
                         'El número de poliza ha sido actualizado y el usuario ha sido notificados')


poliza_lista = Signal()
poliza_lista.connect(notificar_poliza_lista)


def renovar_poliza(sender, **kwargs):
    request = kwargs.get('request')
    fecha_renovacion = kwargs.pop('fecha_renovacion', None)
    if not fecha_renovacion:
        fecha_renovacion = datetime.now()
    nueva = Poliza(no_poliza=sender.no_poliza, aseguradora=sender.aseguradora,
                   contratante=sender.contratante, cliente=sender.cliente,
                   grupo=sender.grupo, ramo=sender.ramo, sub_ramo=sender.sub_ramo,
                   tipo_poliza=sender.tipo_poliza, estado_poliza=EstadoPoliza.PENDIENTE,
                   fecha_emision=fecha_renovacion, fecha_vence=fecha_renovacion + timedelta(days=365)
                   )
    if request:
        nueva.user = request.user
    nueva.fecha_pago = None
    nueva.save()
    AddComment.send(nueva, request=request, comentario="Creada en estado pendiente mendiante proceso de renovación")

    for cert in sender.datos_tecnicos.all():
        dato = DatoPoliza(poliza=nueva, extra_data=cert.extra_data)
        dato.save()
    sender.estado_poliza = EstadoPoliza.RENOVADA
    sender.save()

    return nueva


RenovarPoliza = Signal()
RenovarPoliza.connect(renovar_poliza)


def add_comment(sender, **kwargs):
    request = kwargs.get('request')
    comentario = kwargs.get('comentario')
    c = Comentario()
    if request:
        c.created_user = request.user
        c.updated_user = request.user
    c.type = ContentType.objects.get_for_model(sender.__class__)
    c.key = sender.pk
    c.comentario = comentario
    c.save()
    return c


AddComment = Signal()
AddComment.connect(add_comment)


def notificar_tramite(sender, **kwargs):
    request = kwargs.get('request')
    config = get_config(sender.user)
    html = render_to_string('cotizador/email/notificaion_tramite.html',
                            context={'object': sender, 'opts': sender._meta},
                            request=request)
    send_email('Solicitud de baja %s', config.email_trust, html=html)


NotificarTramite = Signal()
NotificarTramite.connect(notificar_tramite)
