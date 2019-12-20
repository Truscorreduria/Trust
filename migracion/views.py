from grappelli_extras.utils import Codec
from django.http import JsonResponse
from migracion.models import *
from cotizador.models import PerfilEmpleado, benSepelio, benAccidente, Poliza, Notificacion
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
from constance import config


def generar_usuario(e, request):
    ### CREAR USUARIO
    try:
        user = User.objects.create_user(username=e.username, password="BanproTrust2019")
        user.email = e.correo
        user.save()
    except:
        messages.error(request, 'Ya exise otro usuario %s' % e.username)
        return JsonResponse({}, encoder=Codec)

    ### CREAR PERFIL
    try:
        p = PerfilEmpleado(user=user)
        p.primer_nombre = e.primer_nombre
        p.segundo_nombre = e.segundo_nombre
        p.apellido_paterno = e.primer_apellido
        p.apellido_materno = e.segundo_apellido
        p.cedula = e.cedula
        p.cambiar_pass = True
        p.codigo_empleado = ""
        p.save()
    except:
        messages.error(request, 'No se logró crear el perfil')
        return JsonResponse({}, encoder=Codec)

    ### CREAR PÓLIZA DE AUTOMOVIL
    if e.automoviles.all().count() == 0:
        messages.info(request, 'No se encontró ninguna póliza de automovil')
    else:
        for a in e.automoviles.all():
            try:
                po = Poliza(user=user)
                po.no_poliza = a.poliza
                po.cedula = a.cedula
                po.nombres = a.contratante
                po.marca = a.marca
                po.modelo = a.modelo
                po.anno = a.anno
                po.placa = a.placa
                po.chasis = a.chasis
                po.motor = a.motor
                po.color = a.color
                po.suma_asegurada = a.suma
                po.suma_asegurada = a.suma
                po.subtotal = a.prima
                po.emision = round((a.prima - config.SOA_AUTOMOVIL) * 0.02, 2)
                po.iva = round(((a.prima + po.emision) - config.SOA_AUTOMOVIL) * 0.15, 2)
                po.total = round(a.prima + po.emision + po.iva, 2)
                po.fecha_emision = datetime.strptime(a.inicio, '%d/%m/%Y')
                po.save()
                no = Notificacion()
                no.poliza = po
                no.fecha = datetime.now()
                no.save()
            except TypeError as err:
                messages.error(request, "Error al crear el la póliza # {0}. Ya que no tiene fecha de emisión o el formato es incorrecto. {1}".format(
                    a.poliza, err
                ))
            except ValueError as err:
                messages.error(request, "Error al crear el la póliza # {0}. Ya que no tiene fecha de emisión o el formato es incorrecto. {1}".format(
                    a.poliza, err
                ))

    ### CREAR BENEFICIARIOS DE SEPELIO
    if e.sepelios.all().exclude(parentesco='TITULAR').count() == 0:
        messages.info(request, 'No se encontró ningún beneficiario de sepelio además del titular.')
    else:

        for s in e.sepelios.all().exclude(parentesco='TITULAR'):
            try:
                bs = benSepelio(empleado=p)
                bs.primer_nombre = s.primer_nombre
                bs.segundo_nombre = s.segundo_nombre
                bs.apellido_paterno = s.primer_apellido
                bs.apellido_materno = s.segundo_apellido
                bs.fecha_nacimiento = datetime.strptime(s.nacimiento, '%Y-%m-%d')
                bs.parentesco = s.parentesco
                bs.save()
                no = Notificacion()
                no.bensepelio = bs
                no.fecha = datetime.now()
                no.save()
            except ValueError as err:
                messages.error(request, "Error al crear el beneficiario de sepelio {0} {1}. {2}".format(
                    s.primer_nombre, s.primer_apellido, err
                ))
            except TypeError as err:
                messages.error(request, "Error al crear el beneficiario de sepelio {0} {1}. {2}. Ya que no tiene fecha de nacimiento".format(
                    s.primer_nombre, s.primer_apellido, err
                ))

    ### CREAR BENEFICIARIOS DE ACCIDENTE
    if e.accidentes.all().exclude(parentesco='TITULAR').count() == 0:
        messages.info(request, 'No se encontró ningún beneficiario de accidente además del titular.')
    else:
        for a in e.accidentes.all().exclude(parentesco='TITULAR'):
            try:
                ba = benAccidente(empleado=p)
                ba.primer_nombre = a.primer_nombre
                ba.segundo_nombre = a.segundo_nombre
                ba.apellido_materno = a.segundo_apellido
                ba.apellido_paterno = a.primer_apellido
                ba.fecha_nacimiento = datetime.strptime(a.fechanacimiento, '%d/%m/%Y')
                ba.parentesco = a.parentesco
                ba.save()
                no = Notificacion()
                no.benaccidente = ba
                no.fecha = datetime.now()
                no.save()
            except ValueError as err:
                messages.error(request, "Error al crear el beneficiario de accidente {0} {1}. {2}".format(
                    s.primer_nombre, s.primer_apellido, err
                ))


def usuario_cotizador(request):
    e = Empleado.objects.get(id=request.POST.get('id'))
    generar_usuario(e, request)
    return JsonResponse({}, encoder=Codec)
