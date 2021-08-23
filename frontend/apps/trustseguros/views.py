from django.shortcuts import render
from django.template.loader import render_to_string
from adminlte.generics import Datatables
from django.contrib.auth.decorators import login_required
from backend.utils import calcular_tabla_cuotas, parse_date
from .forms import *
from django.http import JsonResponse
from grappelli_extras.utils import Codec
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from backend.signals import RenovarPoliza
from django.db import IntegrityError
from backend.signals import AddComment
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf
from utils.utils import send_email
from adminlte.utils import Codec
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned


def get_attr(obj, attr_name):
    value = obj
    for attr in attr_name.split('.'):
        try:
            value = getattr(value, attr)()
        except TypeError:
            value = getattr(value, attr)
        except AttributeError:
            value = None
    return value


def parse_float(string, optional=0.0):
    try:
        return float(string.replace(',', ''))
    except ValueError:
        return optional


def group_to_json(group):
    return model_to_dict(group)


Group.add_to_class('to_json', group_to_json)


def documentos(request):
    if request.method == "POST":
        if 'new' in request.POST:
            file = None
            type = ContentType.objects.get(app_label=request.POST.get('app_label'),
                                           model=request.POST.get('model'))
            original = type.get_object_for_this_type(id=int(request.POST.get('id')))
            if original:
                file = Archivo()
                file.created_user = request.user
                file.updated_user = request.user
                document = request.FILES['file']
                file.nombre = document.name
                file.fecha_caducidad = request.POST.get('fecha_caducidad')
                file.archivo = document
                file.type = type
                file.key = original.id
                file.save()
                html = render_to_string('trustseguros/lte/widgets/drive-cliente-row.html', {
                    'file': ArchivoClienteForm(instance=file)
                })
            return JsonResponse({'html': html, 'archivo': file.to_json()}, encoder=Codec)

        if 'update' in request.POST:
            a = Archivo.objects.get(id=int(request.POST.get('id')))
            nombre = request.POST.get('nombre')
            if nombre:
                a.nombre = nombre
            try:
                fecha = datetime.strptime(request.POST.get('fecha'), '%d/%m/%Y')
                a.fecha_caducidad = fecha
            except:
                pass
            try:
                tipo_doc = DocumentType.objects.get(id=request.POST.get('tipo_doc'))
                a.tipo_doc = tipo_doc
            except:
                pass

            a.save()
            return JsonResponse(a.to_json(), encoder=Codec)
        if 'delete' in request.POST:
            Archivo.objects.get(id=int(request.POST.get('id'))).delete()
            return JsonResponse({})


def comentarios(request):
    if request.method == "POST":
        if 'new' in request.POST:
            file = None
            try:
                type = ContentType.objects.get(app_label=request.POST.get('app_label'),
                                               model=request.POST.get('model'))
                original = type.get_object_for_this_type(id=int(request.POST.get('id')))
            except:
                type = None
                original = None
            if original:
                file = Comentario()
                file.created_user = request.user
                file.updated_user = request.user
                file.comentario = request.POST.get('comentario')
                file.type = type
                file.key = original.id
                file.save()
            return JsonResponse({'instance': file.to_json()}, encoder=Codec)


# @staff_member_required
# def certificados(request):
#     return render(request, 'trustseguros/include/certificados.html', {
#         'poliza': Poliza.objects.get(id=int(request.GET.get('poliza'))),
#         'form': CertificadoForm()
#     })
#
#
# @staff_member_required
# def certificado(request):
#     try:
#         print(request.POST.get('id'))
#         instance = get_object_or_404(Certificado, id=int(request.POST.get('id')))
#     except:
#         print("no instance")
#         instance = None
#     form = CertificadoForm(request.POST or None, instance=instance)
#     print(form.is_valid())
#     if form.is_valid():
#         cert = form.save()
#         return JsonResponse(cert.to_json(), encoder=Codec)
#     else:
#         print(form.errors)
#         return JsonResponse({}, encoder=Codec)
#
#
# def format_date(value):
#     return value
#
#
# def try_import(obj, prop, source, value, iter, is_date=False):
#     try:
#         if not source[value][iter] or source[value][iter] == 'nan' or source[value][iter] == '-' or source[value][
#             iter] == '.':
#             obj[prop] = None
#         else:
#             if is_date:
#                 print(format_date(source[value][iter]))
#                 obj[prop] = format_date(source[value][iter])
#             obj[prop] = source[value][iter]
#     except:
#         pass
#
#
# def smart_key(options, value):
#     for obj in options:
#         if obj[1] == value:
#             return obj[0]
#     return None
#
#
# def get_aseguradora(name):
#     a, _ = Aseguradora.objects.get_or_create(nombre=name)
#     return a
#
#
# def get_ramo(name):
#     r, _ = Ramo.objects.get_or_create(nombre=name)
#     return r
#
#
# def get_subramo(name, ramo):
#     r = get_ramo(ramo)
#     r.save()
#     sr, _ = SubRamo.objects.get_or_create(nombre=name, ramo=r)
#     sr.save()
#     return sr
#
#
# def get_cliente(tipo, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, genero, tipo_identificacion,
#                 numero_identificacion, vecimiento_documento, fecha_nacimiento, estado_civil, ocupacion,
#                 razon_social, ruc, fecha_expedicion, fecha_constitucion, actividad_economica):
#     if smart_key(TIPOS_CLIENTE, tipo) == Cliente.NATURAL:
#         c, _ = Cliente.objects.get_or_create(tipo=Cliente.NATURAL,
#                                              tipo_identificacion=smart_key(
#                                                  Cliente.TIPOS_IDENTIFICACION, tipo_identificacion),
#                                              numero_identificacion=numero_identificacion)
#         c.genero = smart_key(Cliente.GENEROS, genero)
#         c.primer_nombre = primer_nombre
#         c.segundo_nombre = segundo_nombre
#         c.primer_apellido = primer_apellido
#         c.segundo_apellido = segundo_apellido
#         c.vecimiento_documento = vecimiento_documento
#         c.fecha_nacimiento = fecha_nacimiento
#         c.estado_civil = estado_civil
#         c.ocupacion = ocupacion
#         c.save()
#         return c
#     if smart_key(TIPOS_CLIENTE, tipo) == Cliente.JURIDICO:
#         c, _ = Cliente.objects.get_or_create(tipo=Cliente.JURIDICO,
#                                              ruc=ruc)
#         c.razon_social = razon_social
#         c.fecha_expedicion = format_date(fecha_expedicion)
#         c.fecha_constitucion = format_date(fecha_constitucion)
#         c.actividad_economica = actividad_economica
#         c.save()
#         return c
#
#
# def get_vendedor(name):
#     v, _ = Vendedor.objects.get_or_create(nombre=name)
#     return v
#
#
# def importar_polizas(request):
#     data = pd.read_excel(request.FILES['file'])
#     data = data.replace(np.nan, '')
#     dict_data = data.to_dict('index')
#     success = []
#     for n in range(0, len(data['numero_poliza'])):
#         o = dict_data[n]
#         form = ImportPolizaForm(o)
#         if form.is_valid():
#             form.save()
#             success.append(form.instance)
#         else:
#             err_values = list(form.errors.values())
#             err = "Línea # " + str(n + 2)
#             for nn, e in enumerate(list(form.errors.keys())):
#                 err += " %s %s" % (e, " ".join(err_values[nn]))
#             err += " Esta linea no se importó!"
#             messages.error(request, err)
#
#     messages.success(request, "%s empresas polizas con éxito." % len(success))
#     return JsonResponse({}, encoder=Codec)
#
#
# class ImportMixin:
#     title = ""
#     import_template = ""
#     form = None
#     template = ""
#
#     def _to_dict(self, qdict):
#         return {k: v for k, v in qdict.lists()}
#
#     def get_fields(self):
#         return self.form().fields
#
#     def dtypes(self):
#         return {field: str for field in self.get_fields()}
#
#     def get(self, request):
#         return render(request, "trustseguros/admin/import.html", {
#             'title': self.title, 'forms': [], 'fields': self.get_fields(),
#             'form': self.form, 'template': self.template
#         })
#
#
# class ImportCompany(View, ImportMixin):
#     title = "Importar clientes jurídicos"
#     form = ImportEmpresaForm
#     template = "cliente_juridico.xlsx"
#
#     def post(self, request):
#         form_list = []
#         error_list = []
#         if 'apply' in request.POST:
#             data = self._to_dict(request.POST)
#             print(data)
#             del data['csrfmiddlewaretoken']
#             del data['apply']
#             for n, t in enumerate(data['tipo']):
#                 o = dict()
#                 for field in data.keys():
#                     try:
#                         o[field] = data[field][n]
#                     except:
#                         print(data[field])
#                 form = self.form(o)
#                 if form.is_valid():
#                     form.save()
#                     form_list.append(form)
#                 else:
#                     error_list.append(form)
#             messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
#             if len(error_list) > 0:
#                 messages.error(request, "%s empresas produjeron error!" % len(error_list))
#                 return render(request, "trustseguros/admin/import.html", {
#                     'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
#                     'form': self.form, 'template': self.template
#                 })
#             return HttpResponseRedirect('/admin/trustseguros/cliente/')
#         else:
#             data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
#             data = data.replace(np.nan, '')
#             dict_data = data.to_dict('index')
#             for n in range(0, len(data['razon_social'])):
#                 o = dict_data[n]
#                 o['tipo'] = 2
#                 form = self.form(o)
#                 form.is_valid()
#                 form_list.append(form)
#         return render(request, "trustseguros/admin/import-table.html", {
#             'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
#         })
#
#
# class ImportPerson(View, ImportMixin):
#     title = "Importar personas naturales"
#     form = ImportPersonaForm
#     template = "cliente_natural.xlsx"
#
#     def post(self, request):
#         form_list = []
#         error_list = []
#         if 'apply' in request.POST:
#             data = self._to_dict(request.POST)
#             print(data)
#             del data['csrfmiddlewaretoken']
#             del data['apply']
#             for n, t in enumerate(data['tipo']):
#                 o = dict()
#                 for field in data.keys():
#                     try:
#                         o[field] = data[field][n]
#                     except:
#                         print(data[field])
#                 form = self.form(o)
#                 if form.is_valid():
#                     form.save()
#                     form_list.append(form)
#                 else:
#                     error_list.append(form)
#             messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
#             if len(error_list) > 0:
#                 messages.error(request, "%s empresas produjeron error!" % len(error_list))
#                 return render(request, "trustseguros/admin/import.html", {
#                     'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
#                     'form': self.form
#                 })
#             return HttpResponseRedirect('/admin/trustseguros/cliente/')
#         else:
#             data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
#             data = data.replace(np.nan, '')
#             dict_data = data.to_dict('index')
#             for n in range(0, len(data['primer_nombre'])):
#                 o = dict_data[n]
#                 o['tipo'] = 1
#                 form = self.form(o)
#                 form.is_valid()
#                 form_list.append(form)
#         return render(request, "trustseguros/admin/import-table.html", {
#             'forms': form_list, 'form': self.form, 'fields': self.get_fields()
#         })
#
#
# class ImportPoliza(View, ImportMixin):
#     title = "Importar pólizas"
#     form = ImportPolizaForm
#     template = "poliza.xlsx"
#
#     def post(self, request):
#         form_list = []
#         error_list = []
#         if 'apply' in request.POST:
#             data = self._to_dict(request.POST)
#             print(data)
#             del data['csrfmiddlewaretoken']
#             del data['apply']
#             for n, t in enumerate(data['numero_poliza']):
#                 o = dict()
#                 for field in data.keys():
#                     try:
#                         o[field] = data[field][n]
#                     except:
#                         print(data[field])
#                 form = self.form(o)
#                 if form.is_valid():
#                     form.save()
#                     form_list.append(form)
#                 else:
#                     error_list.append(form)
#             messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
#             if len(error_list) > 0:
#                 messages.error(request, "%s empresas produjeron error!" % len(error_list))
#                 return render(request, "trustseguros/admin/import.html", {
#                     'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
#                     'form': self.form, 'template': self.template
#                 })
#             return HttpResponseRedirect('/admin/trustseguros/poliza/')
#         else:
#             data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
#             data = data.replace(np.nan, '')
#             dict_data = data.to_dict('index')
#             for n in range(0, len(data['numero_poliza'])):
#                 o = dict_data[n]
#                 form = self.form(o)
#                 form.is_valid()
#                 form_list.append(form)
#         return render(request, "trustseguros/admin/import-table.html", {
#             'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
#         })
#
#
# class ImportCertificadoEdificio(View, ImportMixin):
#     title = "Importar certificados de edificios"
#     form = ImportCertificadoEdificioForm
#     template = "certificado_edificio.xlsx"
#
#     def post(self, request):
#         form_list = []
#         error_list = []
#         if 'apply' in request.POST:
#             data = self._to_dict(request.POST)
#             del data['csrfmiddlewaretoken']
#             del data['apply']
#             for n, t in enumerate(data['numero_poliza']):
#                 o = dict()
#                 for field in data.keys():
#                     try:
#                         o[field] = data[field][n]
#                     except:
#                         print(data[field])
#                 form = self.form(o)
#                 if form.is_valid():
#                     form.save()
#                     form_list.append(form)
#                 else:
#                     error_list.append(form)
#             messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
#             if len(error_list) > 0:
#                 messages.error(request, "%s empresas produjeron error!" % len(error_list))
#                 return render(request, "trustseguros/admin/import.html", {
#                     'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
#                     'form': self.form, 'template': self.template
#                 })
#             return HttpResponseRedirect('/admin/trustseguros/certificado/')
#         else:
#             data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
#             data = data.replace(np.nan, '')
#             dict_data = data.to_dict('index')
#             for n in range(0, len(data['numero_poliza'])):
#                 o = dict_data[n]
#                 o['tipo'] = 'edificio'
#                 form = self.form(o)
#                 form.is_valid()
#                 form_list.append(form)
#         return render(request, "trustseguros/admin/import-table.html", {
#             'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
#         })
#
#
# class ImportCertificadoAuto(View, ImportMixin):
#     title = "Importar certificados de autos"
#     form = ImportCertificadoAutoForm
#     template = "certificado_auto.xlsx"
#
#     def post(self, request):
#         form_list = []
#         error_list = []
#         if 'apply' in request.POST:
#             data = self._to_dict(request.POST)
#             print(data)
#             del data['csrfmiddlewaretoken']
#             del data['apply']
#             for n, t in enumerate(data['numero_poliza']):
#                 o = dict()
#                 for field in data.keys():
#                     try:
#                         o[field] = data[field][n]
#                     except:
#                         print(data[field])
#                 form = self.form(o)
#                 if form.is_valid():
#                     form.save()
#                     form_list.append(form)
#                 else:
#                     error_list.append(form)
#             messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
#             if len(error_list) > 0:
#                 messages.error(request, "%s empresas produjeron error!" % len(error_list))
#                 return render(request, "trustseguros/admin/import.html", {
#                     'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
#                     'form': self.form, 'template': self.template
#                 })
#             return HttpResponseRedirect('/admin/trustseguros/certificado/')
#         else:
#             data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
#             data = data.replace(np.nan, '')
#             dict_data = data.to_dict('index')
#             for n in range(0, len(data['numero_poliza'])):
#                 o = dict_data[n]
#                 o['tipo'] = 'auto'
#                 form = self.form(o)
#                 form.is_valid()
#                 form_list.append(form)
#         return render(request, "trustseguros/admin/import-table.html", {
#             'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
#         })
#
#
# class ImportCertificadoPersona(View, ImportMixin):
#     title = "Importar certificados de personas"
#     form = ImportCertificadoPersonaForm
#     template = "certificado_persona.xlsx"
#
#     def post(self, request):
#         form_list = []
#         error_list = []
#         if 'apply' in request.POST:
#             data = self._to_dict(request.POST)
#             print(data)
#             del data['csrfmiddlewaretoken']
#             del data['apply']
#             for n, t in enumerate(data['numero_poliza']):
#                 o = dict()
#                 for field in data.keys():
#                     try:
#                         o[field] = data[field][n]
#                     except:
#                         print(data[field])
#                 form = self.form(o)
#                 if form.is_valid():
#                     form.save()
#                     form_list.append(form)
#                 else:
#                     error_list.append(form)
#             messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
#             if len(error_list) > 0:
#                 messages.error(request, "%s empresas produjeron error!" % len(error_list))
#                 return render(request, "trustseguros/admin/import.html", {
#                     'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
#                     'form': self.form, 'template': self.template
#                 })
#             return HttpResponseRedirect('/admin/trustseguros/certificado/')
#         else:
#             data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
#             data = data.replace(np.nan, '')
#             dict_data = data.to_dict('index')
#             for n in range(0, len(data['numero_poliza'])):
#                 o = dict_data[n]
#                 o['tipo'] = 'persona'
#                 form = self.form(o)
#                 form.is_valid()
#                 form_list.append(form)
#         return render(request, "trustseguros/admin/import-table.html", {
#             'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
#         })
#
#
# def download(request):
#     file_name = request.POST.get('file_name', request.GET.get('file_name'))
#     path_to_file = os.path.join(settings.STATIC_ROOT, 'descargas', file_name)
#     if os.path.exists(path_to_file):
#         with open(path_to_file, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type='application/force-download')
#             response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(file_name)
#             response['X-Sendfile'] = path_to_file
#             return response
#     else:
#         raise Http404


@login_required(login_url="/cotizador/login/")
def index(request):
    def get_ejecutivo(poliza):
        if poliza.ejecutivo:
            return poliza.ejecutivo
        return ""

    def cuota_json(cuota):
        return {
            'id': cuota.id,
            'id_poliza': cuota.poliza.id,
            'no_poliza': cuota.poliza.no_poliza,
            'ejecutivo': get_ejecutivo(cuota.poliza),
            'cliente': get_attr(cuota, 'poliza.cliente.get_full_name'),
            'contratante': get_attr(cuota, 'poliza.contratante.get_full_name'),
            'prima': cuota.monto,
            'comision': cuota.monto_comision,
            'monto_pagado': cuota.monto_pagado(),
            'fecha_vence': cuota.fecha_vence,
        }

    def poliza_json(poliza):
        return {
            'id': poliza.id,
            'no_poliza': poliza.no_poliza,
            'fecha_emision': poliza.fecha_emision,
            'fecha_vence': poliza.fecha_vence,
            'prima': poliza.prima_total(),
            'comision': poliza.comision_total(),
            'ejecutivo': get_ejecutivo(poliza),
            'cliente': get_attr(poliza, 'cliente.get_full_name'),
            'contratante': get_attr(poliza, 'contratante.get_full_name'),
            'grupo': get_attr(poliza, 'grupo.name'),
        }

    def cartera(coin, group):
        polizas = Poliza.objects.filter(moneda=coin, estado_poliza=EstadoPoliza.ACTIVA)
        if group:
            polizas = Poliza.objects.filter(moneda=coin, estado_poliza=EstadoPoliza.ACTIVA, grupo=group)
        return [cuota_json(cuota) for cuota in Cuota.objects.filter(poliza__in=polizas,
                                                                    estado__in=[EstadoPago.VIGENTE,
                                                                                EstadoPago.VENCIDO]
                                                                    ).order_by('fecha_vence')]

    def vencimiento(coin, group):
        if group:
            return [poliza_json(p) for p in Poliza.objects.filter(
                estado_poliza=EstadoPoliza.ACTIVA, moneda=coin,
                grupo=group)]
        return [poliza_json(p) for p in Poliza.objects.filter(
            estado_poliza=EstadoPoliza.ACTIVA, moneda=coin)]

    def oportunidad_to_json(oportunidad):
        return {
            'id': get_attr(oportunidad, 'id'),
            'campain': get_attr(oportunidad, 'campain.name'),
            'linea': get_attr(oportunidad, 'linea.name'),
            'status': get_attr(oportunidad, 'get_status_display'),
            'valor_nuevo': get_attr(oportunidad, 'valor_nuevo'),
            'valor_exceso': get_attr(oportunidad, 'valor_exceso'),
            **oportunidad.data_load()
        }

    if request.method == 'POST':
        form = DashboardFiltersForm(request.POST)
        response = {}
        if 'crm' in request.POST:
            if form.is_valid():
                response = {
                    'oportunidades': [x.to_json() for x in Oportunity.objects.filter(
                        created__gte=form.cleaned_data['desde'],
                        created__lte=form.cleaned_data['hasta'],
                    )],
                }
        if 'siniestros' in request.POST:
            response = {
                'siniestros': [x.to_json() for x in Siniestro.objects.all()],
            }
        if 'cartera' in request.POST:
            form.is_valid()
            for moneda in Moneda.objects.all():
                response['cartera_' + moneda.moneda] = cartera(moneda, form.cleaned_data['grupo'])
        if 'vencimiento' in request.POST:
            form.is_valid()
            for moneda in Moneda.objects.all():
                response['vencimiento_' + moneda.moneda] = vencimiento(moneda, form.cleaned_data['grupo'])
        if 'canceladas' in request.POST:
            if form.is_valid():
                response = {
                    'canceladas': [poliza_json(poliza) for poliza in Poliza.objects.filter(
                        estado_poliza=EstadoPoliza.CANCELADA,
                        fecha_cancelacion__gte=form.cleaned_data['desde'],
                        fecha_cancelacion__lte=form.cleaned_data['hasta'],
                    )]
                }

        return JsonResponse(response, encoder=Codec)

    return render(request, 'adminlte/index.html', {'filter_form': DashboardFiltersForm})


@login_required(login_url="/cotizador/login/")
def profile(request):
    return render(request, 'trustseguros/lte/profile.html', {

    })


def tabla_cuotas(instance, request):
    total = float(request.POST.get('total', '0').replace(',', ''))
    prima_neta = float(request.POST.get('prima_neta', '0').replace(',', ''))
    per_comision = float(request.POST.get('per_comision', '0').replace(',', ''))
    fecha_pago = datetime.strptime(request.POST.get('fecha_pago'), '%d/%m/%Y')
    cuotas = int(request.POST.get('cantidad_cuotas'))
    return calcular_tabla_cuotas(prima_neta, per_comision, total, fecha_pago, cuotas, instance)


# region Clientes

class PersonaNatural(Datatables):
    modal_width = 1400
    model = ClienteNatural
    form = ClienteNaturalForm
    list_display = ('primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'cedula')
    search_fields = ('primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'cedula')
    list_filter = ('departamento',)
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información General',
            'fields': (
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('genero', 'estado_civil'),
                ('tipo_identificacion', 'cedula'),
                ('telefono', 'celular', 'email_personal'),
                ('departamento', 'municipio'),
                ('domicilio',),
            )
        },
        {
            'id': 'empleo',
            'name': 'Información laboral',
            'fields': (
                ('empresa', 'sucursal'),
                ('codigo_empleado', 'cargo'),
            )
        },
        {
            'id': 'sistema',
            'name': 'Accesso al sistema',
            'fields': (
                ('user', 'cambiar_pass',),
            )
        },
        {
            'id': 'polizas_activas',
            'name': 'Pólizas Activas',
            'fields': (
                ('polizas',),
            )
        },
        {
            'id': 'historial_polizas',
            'name': 'Pólizas Histórico',
            'fields': (
                ('polizas_renovadas',),
            )
        },
        {
            'id': 'documentos',
            'name': 'Documentos',
            'fields': (
                ('documentos',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/lte/js/municipio.js', 'trustseguros/lte/js/cliente.add.poliza.js',
               'trustseguros/lte/js/cliente.documentos.js']
    }

    def get_buttons(self, request, instance=None):
        if instance.id:
            return [
                {
                    'class': 'btn btn-warning btn-perform',
                    'perform': 'save',
                    'callback': 'add_poliza',
                    'icon': 'fa fa-exclamation-triangle',
                    'text': 'Añadir póliza',
                },
                {
                    'class': 'btn btn-success btn-perform',
                    'perform': 'save',
                    'callback': 'process_response',
                    'icon': 'fa fa-save',
                    'text': 'Guardar',
                },
            ]
        return super().get_buttons(request, instance=instance)


class PersonaJuridica(Datatables):
    modal_width = 1400
    model = ClienteJuridico
    form = ClienteJuridicioForm
    list_display = ('razon_social', 'ruc', 'actividad_economica', 'pagina_web')
    search_fields = ('razon_social', 'ruc', 'actividad_economica', 'pagina_web')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información General',
            'fields': (
                ('razon_social', 'ruc'),
                ('nombre_comercial', 'actividad_economica'),
                ('telefono', 'pagina_web'),
                ('es_cesionario',),
                ('departamento', 'municipio'),
                ('domicilio',),
            )
        },
        {
            'id': 'representante-legal',
            'name': 'Datos del represante legal',
            'fields': (
                ('representante',),
            )
        },
        {
            'id': 'contacts',
            'name': 'Contactos',
            'fields': (
                ('contactos',),
            )
        },
        {
            'id': 'polizas_activas',
            'name': 'Pólizas Activas',
            'fields': (
                ('polizas',),
            )
        },
        {
            'id': 'historial_polizas',
            'name': 'Pólizas Histórico',
            'fields': (
                ('polizas_renovadas',),
            )
        },
        {
            'id': 'documentos',
            'name': 'Documentos',
            'fields': (
                ('documentos',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/lte/js/municipio.js', 'trustseguros/lte/js/municipio-representante.js',
               'trustseguros/lte/js/autocomplete-representante.js', 'trustseguros/lte/js/cliente.add.poliza.js',
               'trustseguros/lte/js/cliente.documentos.js']
    }

    def get_buttons(self, request, instance=None):
        if instance.id:
            return [
                {
                    'class': 'btn btn-warning btn-perform',
                    'perform': 'save',
                    'callback': 'add_poliza',
                    'icon': 'fa fa-exclamation-triangle',
                    'text': 'Añadir póliza',
                },
                {
                    'class': 'btn btn-success btn-perform',
                    'perform': 'save',
                    'callback': 'process_response',
                    'icon': 'fa fa-save',
                    'text': 'Guardar',
                },
            ]
        return super().get_buttons(request, instance=instance)

    def save_related(self, instance, data):
        try:
            rf = RepresentanteForm(data,
                                   instance=ClienteNatural.objects.get(
                                       cedula=data.get('cliente_representante-cedula')))
        except ObjectDoesNotExist as error:
            print(error)
            rf = RepresentanteForm(data)
        if rf.is_valid():
            rf.save()
        else:
            print(rf.errors)
        instance.representante = rf.instance
        instance.save()
        for i in range(1, len(data.getlist('contacto_id'))):
            if data.getlist('contacto_id')[i] == '':
                c = Contacto(contacto=instance)
            else:
                c = Contacto.objects.get(id=int(data.getlist('contacto_id')[i]))
            c.primer_nombre = data.getlist('cliente_contacto-primer_nombre')[i]
            c.segundo_nombre = data.getlist('cliente_contacto-segundo_nombre')[i]
            c.apellido_paterno = data.getlist('cliente_contacto-apellido_paterno')[i]
            c.apellido_materno = data.getlist('cliente_contacto-apellido_materno')[i]
            c.cedula = data.getlist('cliente_contacto-cedula')[i]
            c.telefono = data.getlist('cliente_contacto-telefono')[i]
            c.celular = data.getlist('cliente_contacto-celular')[i]
            c.email_personal = data.getlist('cliente_contacto-email_personal')[i]
            c.save()


# endregion


# region Catálogos


class Lineas(Datatables):
    model = Linea
    form = LineaForm
    list_display = ('name',)


class Campains(Datatables):
    model = Campain
    form = CampainForm
    list_display = ('name', ('Línea', 'linea.name'), 'active')
    list_filter = ('linea', 'active')


class Aseguradoras(Datatables):
    modal_width = 900
    model = Aseguradora
    form = AseguradoraForm
    list_display = ('code', 'name', 'phone', 'address', 'emision', 'emision_min', 'monto_soa', 'exceso')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('code', 'name'),
                ('ruc', 'phone', 'email'),
                ('emision', 'exceso', 'tarifa'),
                ('coaseguro_robo', 'coaseguro_dano', 'deducible'),
                ('emision_soa', 'emision_min', 'monto_soa'),
                ('calc_alt',),
                ('sorcv', 'csorcv', 'cdp'),
                ('address',),
            )
        },
        {
            'id': 'tabla-depreciacion',
            'name': 'Tabla de depreciación',
            'fields': (
                ('depreciacion',),
            )
        },
        {
            'id': 'contactos',
            'name': 'Contactos aseguradora',
            'fields': (
                ('contactos',),
            )
        },
    ]

    def save_related(self, instance, data):
        for i in range(1, len(data.getlist('contactoaseguradora_id'))):
            if data.getlist('contactoaseguradora_id')[i] == '':
                c = ContactoAseguradora(aseguradora=instance)
            else:
                c = ContactoAseguradora.objects.get(id=int(data.getlist('contactoaseguradora_id')[i]))
            c.name = data.getlist('contacto_aseguradora-name')[i]
            c.save()


class Ramos(Datatables):
    model = Ramo
    form = RamoForm
    list_display = ('name',)
    search_fields = ('name',)
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('name',),
            )
        },
    ]


class Grupos(Datatables):
    model = Grupo
    list_display = ('name', 'email_notificacion')
    search_fields = ('name',)
    fields = ('name', 'autorenovacion', 'email_notificacion')


class SubRamos(Datatables):
    modal_width = 1300
    model = SubRamo
    form = SubRamoForm
    list_display = ('name', 'ramo.name')
    search_fields = ('name',)
    list_filter = ('ramo',)
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('name', 'ramo'),
                ('show_quotation',),
            )
        },
        {
            'id': 'coberturas',
            'name': 'Coberturas que aplica',
            'fields': (
                ('coberturas',),
            )
        },
        {
            'id': 'datos-tecnicos',
            'name': 'Datos técnicos',
            'fields': (
                ('campos_adicionales',),
            )
        },
    ]

    def save_related(self, instance, data):
        for i in range(1, len(data.getlist('cobertura_id'))):
            if data.getlist('cobertura_id')[i] == '':
                c = Cobertura(sub_ramo=instance)
            else:
                c = Cobertura.objects.get(id=int(data.getlist('cobertura_id')[i]))
            f = CoberturaForm({
                'subramo_cobertura-name': data.getlist('subramo_cobertura-name')[i],
                'subramo_cobertura-en_cotizacion': data.getlist('subramo_cobertura-en_cotizacion')[i],
                # 'subramo_cobertura-tipo_calculo': data.getlist('subramo_cobertura-tipo_calculo')[i],
                # 'subramo_cobertura-tipo_cobertura': data.getlist('subramo_cobertura-tipo_cobertura')[i],
                # 'subramo_cobertura-tipo_exceso': data.getlist('subramo_cobertura-tipo_exceso')[i],
                # 'subramo_cobertura-iva': data.getlist('subramo_cobertura-iva')[i],
            }, instance=c)
            if f.is_valid():
                f.save()

        for i in range(1, len(data.getlist('campoadicional_id'))):
            if data.getlist('campoadicional_id')[i] == '':
                c = CampoAdicional(sub_ramo=instance)
            else:
                c = CampoAdicional.objects.get(id=int(data.getlist('campoadicional_id')[i]))
            f = CampoAdicionalForm({
                'ramo_campo_adicional-order': data.getlist('ramo_campo_adicional-order')[i],
                'ramo_campo_adicional-name': data.getlist('ramo_campo_adicional-name')[i],
                'ramo_campo_adicional-label': data.getlist('ramo_campo_adicional-label')[i],
            }, instance=c)
            if f.is_valid():
                f.save()

        for i in range(0, len(data.getlist('valor_cobertura_cobertura'))):
            aseguradora = Aseguradora.objects.get(id=data.getlist('valor_cobertura_aseguradora')[i])
            cobertura = Cobertura.objects.get(id=data.getlist('valor_cobertura_cobertura')[i])
            valor_cobertura, created = CoberturaAseguradora.objects.get_or_create(
                aseguradora=aseguradora, cobertura=cobertura
            )
            valor_cobertura.valor = data.getlist('valor_cobertura_valor')[i]
            valor_cobertura.save()


class Tarifas(Datatables):
    model = Tarifa
    form = TarifaForm
    list_display = ('marca', 'modelo', 'exceso', 'tarifa', 'coaseguro_robo', 'coaseguro_dano', 'deducible',
                    ('Aseguradora', 'aseguradora.name'))
    list_filter = ('aseguradora',)
    search_fields = ('marca', 'modelo')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('aseguradora', 'tarifa'),
                ('marca', 'modelo'),
                ('exceso', 'deducible'),
                ('coaseguro_robo', 'coaseguro_dano'),
            )
        },
    ]


class TiposDocumentos(Datatables):
    model = DocumentType
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)


# endregion


# region Pólizas

class Polizas(Datatables):
    modal_width = 1600
    model = Poliza
    form = PolizaForm
    list_template = 'trustseguros/lte/poliza-datatables.html'
    form_template = 'trustseguros/lte/poliza-modal.html'
    list_display = ('no_poliza', 'cliente.name', 'aseguradora.name', 'ramo.name', ('Fecha de inicio', 'fecha_emision'),
                    ('Fecha fin', 'fecha_vence'), ('Dias para vencimiento', 'dias_vigencia'), 'grupo.name',
                    'suma_asegurada', ('Prima neta', 'total'), 'tipo_poliza.label', 'estado_poliza.label')
    search_fields = ('no_poliza', 'no_recibo', 'nombres', 'apellidos')
    list_filter = ('estado_poliza', 'grupo', 'sub_ramo')
    media = {
        'js': ['trustseguros/lte/js/fecha-vence.js', ],
        'css': ['trustseguros/lte/css/coberturas-field.css', 'trustseguros/lte/css/recibo.fields.localize.css', ]
    }

    def get_queryset(self, filters, search_value):
        return super().get_queryset(filters, search_value).filter(
            estado_poliza__in=[EstadoPoliza.PENDIENTE, EstadoPoliza.ACTIVA])

    def get_buttons(self, request, instance=None):
        buttons = self.buttons.copy()
        if instance.id:
            if instance.editable:
                buttons.append({
                    'class': 'btn btn-info btn-perform',
                    'icon': 'fa fa-suitcase',
                    'text': 'Finalizar',
                    'perform': 'activar',
                    'callback': 'process_response',
                })
            else:
                if instance.estado_poliza in [EstadoPoliza.ACTIVA, EstadoPoliza.PENDIENTE]:
                    buttons = [{
                        'class': 'btn btn-default btn-norenew',
                        'icon': 'fa fa-fan',
                        'text': 'No Renovar',
                    }, {
                        'class': 'btn btn-info btn-renew',
                        'icon': 'fa fa-fan',
                        'text': 'Renovar',
                    }, {
                        'class': 'btn btn-warning btn-perform',
                        'icon': 'fa fa-edit',
                        'text': 'Modificar',
                        'perform': 'modificando',
                        'callback': 'process_response',
                    }, {
                        'class': 'btn btn-danger btn-null',
                        'icon': 'fa fa-exclamation-triangle',
                        'text': 'Cancelar',
                    }
                    ]
                else:
                    buttons = []

            if instance.modificando:
                buttons = [{
                    'class': 'btn btn-info btn-perform',
                    'icon': 'fa fa-save',
                    'text': 'Guardar',
                    'perform': 'modificar',
                    'callback': 'process_response'
                }]

            if instance.cancelando:
                buttons = [{
                    'class': 'btn btn-info btn-perform',
                    'icon': 'fa fa-save',
                    'text': 'Guardar',
                    'perform': 'cancelar',
                    'callback': 'process_response',
                }]

            if instance.estado in [EstadoPoliza.CANCELADA, EstadoPoliza.RENOVADA, EstadoPoliza.NORENOVADA]:
                buttons = []
        return buttons

    def put(self, request):
        status = 203
        instance = self.model()
        form = self.get_form()()
        html_form = self.html_form(instance, request, form, 'PUT')
        errors = []

        if 'save' in request.PUT:
            try:
                form = self.get_form()(request.PUT)
                if form.is_valid():
                    form.save()
                    instance = form.instance
                    AddComment.send(instance, request=request,
                                    comentario="Creado en estado %s" % instance.get_estado_poliza_display())
                    status = 200
                    self.save_related(instance=instance, data=request.PUT)
                    form = self.get_form()(instance=instance)
                    html_form = self.html_form(instance, request, form, "POST")
                else:
                    errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                    print(errors)
                    html_form = self.html_form(instance, request, form, "PUT")
            except IntegrityError as e:
                print(e)

        return JsonResponse({'instance': instance.to_json(), 'form': html_form,
                             'errors': errors}, status=status, encoder=Codec)

    def post(self, request):
        if 'activar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            AddComment.send(p, request=request,
                            comentario="Actualizado en estado %s" % p.get_estado_poliza_display())
            p.estado_poliza = EstadoPoliza.ACTIVA
            p.editable = False
            p.perdir_comentarios = False
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')

            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'modificando' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))

            AddComment.send(p, request=request,
                            comentario="Se habilita el modo de edición")
            p.editable = True
            p.perdir_comentarios = True
            p.modificando = True
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'modificar' in request.POST:
            status = 200
            errors = []
            p = self.model.objects.get(id=int(request.POST.get('id')))
            form = self.get_form()(request.POST, instance=p)
            if form.is_valid():
                form.save()
                p = form.instance
                AddComment.send(p, request=request,
                                comentario=request.POST.get('pedir_comentarios'))
                p.editable = False
                p.perdir_comentarios = False
                p.modificando = False
                p.save()
                self.save_related(instance=p, data=request.POST)
                form = self.get_form()(instance=p)
            else:
                errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                status = 203
                print(errors)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form, 'errors': errors},
                                encoder=Codec, status=status)
        if 'cancelando' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            AddComment.send(p, request=request,
                            comentario="Preparando poliza para cancelación")
            p.editable = False
            p.perdir_motivo = True
            p.cancelando = True
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'cancelar' in request.POST:
            instance = self.get_instance(request)
            AddComment.send(instance, request=request,
                            comentario="Poliza en estado cancelada")
            instance.estado_poliza = EstadoPoliza.CANCELADA
            instance.editable = False
            instance.perdir_comentarios = False
            instance.cancelando = False
            instance.fecha_cancelacion = datetime.now()
            instance.motivo_cancelacion = request.POST.get('comentarios')
            instance.save()
            form = self.get_form()(instance=instance)
            html_form = self.html_form(instance, request, form, 'POST')
            return self.make_response(instance, html_form, [], 200)
        if 'renovar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            nueva = RenovarPoliza.send(p, request=request)[0][1]
            form = self.get_form()(instance=nueva)
            html_form = self.html_form(nueva, request, form, 'POST')
            return JsonResponse({'instance': nueva.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'norenovar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            p.estado_poliza = EstadoPoliza.NORENOVADA
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'import_data' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            file = request.FILES['file']
            data = pd.read_excel(file)
            forms = []
            for row in data.to_dict('records'):
                d = DatoPoliza(poliza=p)
                d.extra_data = str(row)
                form = DatoImportForm(instance=d)
                forms.append(form)
            html = render_to_string('trustseguros/lte/widgets/import-rows.html', context={
                'forms': forms, 'widget': {'name': 'campos_adicionales'}
            }, request=request)
            return JsonResponse({'html': html}, encoder=Codec, safe=False)
        if 'calcular_tabla_pagos' in request.POST:
            instance = self.get_instance(request)
            data = tabla_cuotas(instance, request)
            return JsonResponse(data, safe=False, encoder=Codec)
        if 'add_from_customer' in request.POST:
            customer = Cliente.objects.get(id=request.POST.get('customer'))
            p = Poliza()
            p.cliente = customer
            p.save()
            return JsonResponse({'id': p.id}, encoder=Codec)
        return super().post(request)

    def save_related(self, instance, data):

        for i in range(0, len(data.getlist('cobertura'))):
            cobertura = Cobertura.objects.get(id=data.getlist('cobertura')[i])
            monto = float(data.getlist('monto')[i].replace(',', ''))
            if monto > 0:
                r, created = CoberturaPoliza.objects.get_or_create(poliza=instance, cobertura=cobertura)
                r.monto = monto
                r.save()

        for i in range(1, len(data.getlist('campos_adicionales_id'))):
            if data.getlist('campos_adicionales_id')[i] == '':
                c = DatoPoliza(poliza=instance)
            else:
                c = DatoPoliza.objects.get(id=int(data.getlist('campos_adicionales_id')[i]))
            c.extra_data = data.getlist('campos_adicionales')[i].replace('\\', '')
            c.save()

        for i in range(0, len(data.getlist('tabla_pagos_id'))):
            if data.getlist('tabla_pagos_id')[i] == '':
                p = Cuota(poliza=instance)
            else:
                p = Cuota.objects.get(id=int(data.getlist('tabla_pagos_id')[i]))
            p.numero = data.getlist('tabla_pagos_numero')[i]
            p.monto = data.getlist('tabla_pagos_monto')[i].replace(',', '')
            p.fecha_vence = parse_date(data.getlist('tabla_pagos_fecha_vence')[i])
            p.monto_comision = data.getlist('tabla_pagos_monto_comision')[i].replace(',', '')
            p.save()


class Tramites(Datatables):
    modal_width = 1200
    model = Tramite
    form = TramiteForm
    form_template = "trustseguros/lte/tramite-modal.html"
    list_display = ('code', 'tipo_tramite.name', ('Cliente', 'cliente.name'),
                    ('Ingresado por', 'user.username'), ('Poliza', 'poliza.number'),
                    ('Fecha de registro', 'created'), ('Estado', 'estado.name'))
    list_filter = ('tipo_tramite', 'estado', 'user')
    search_fields = ('code', 'cliente__nombre', 'poliza__no_poliza')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Datos del cliente',
            'fields': (
                ('code', 'fecha', 'hora', 'tipo_tramite'),
                ('cliente', 'poliza', 'ramo'),
                ('sub_ramo', 'grupo', 'aseguradora', 'contacto_aseguradora'),
                ('solicitado_por', 'medio_solicitud', 'estado', 'user'),
                ('descripcion', 'genera_endoso', 'remplaza_recibo'),
            )
        },
        {
            'id': 'drive',
            'name': 'Soportes',
            'fields': (
                ('drive',),
            )
        },
        {
            'id': 'bita',
            'name': 'Bitácora',
            'fields': (
                ('bitacora',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/js/tramite.anular.js', 'trustseguros/js/tramite.finalizar.js',
               'trustseguros/js/tramite.soportes.js', 'trustseguros/js/tramite.bitacora.js',
               'trustseguros/js/tramite.poliza.js', 'trustseguros/js/tramite.tablapagos.js', ],
        'css': ['trustseguros/lte/css/recibo.fields.localize.css', ]
    }

    def post(self, request):
        if 'finalizar' in request.POST:
            p = Tramite.objects.get(id=request.POST.get('id'))
            p.editable = False
            p.estado = "En Proceso"
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'activar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            p.estado_poliza = EstadoPoliza.ACTIVA
            p.editable = False
            p.perdir_comentarios = False
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'modificar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            p.editable = True
            p.perdir_comentarios = True
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'confirmar' in request.POST:
            status = 200
            errors = []
            p = self.model.objects.get(id=int(request.POST.get('id')))
            form = self.get_form()(request.POST, instance=p)
            if form.is_valid():
                form.save()
                p = form.instance
                p.editable = False
                p.perdir_comentarios = False
                p.save()
                self.save_related(instance=p, data=request.POST)
                form = self.get_form()(instance=p)
            else:
                errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                status = 203
                print(errors)
            html_form = self.html_form(p, request, form, 'POST')

            return JsonResponse({'instance': p.to_json(), 'form': html_form, 'errors': errors},
                                encoder=Codec, status=status)
        if 'cancelar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            p.estado_poliza = EstadoPoliza.CANCELADA
            p.editable = False
            p.perdir_comentarios = True
            p.save()
            form = self.get_form()(instance=p)
            html_form = self.html_form(p, request, form, 'POST')
            return JsonResponse({'instance': p.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'renovar' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            p.estado_poliza = EstadoPoliza.RENOVADA
            p.save()
            nueva = RenovarPoliza.send(p, request=request)[0][1]
            form = self.get_form()(instance=nueva)
            html_form = self.html_form(nueva, request, form, 'POST')
            return JsonResponse({'instance': nueva.to_json(), 'form': html_form}, encoder=Codec, status=200)
        if 'import_data' in request.POST:
            p = Poliza.objects.get(id=request.POST.get('id'))
            file = request.FILES['file']
            data = pd.read_excel(file)
            forms = []
            for row in data.to_dict('records'):
                d = DatoPoliza(poliza=p)
                d.extra_data = str(row)
                form = DatoImportForm(instance=d)
                forms.append(form)
            html = render_to_string('trustseguros/lte/widgets/import-rows.html', context={
                'forms': forms, 'widget_name': 'campos_adicionales'
            }, request=request)
            return JsonResponse({'html': html}, encoder=Codec, safe=False)
        if 'polizas' in request.POST:
            cliente = Cliente.objects.get(id=request.POST.get('cliente'))
            polizas = Poliza.objects.filter(estado_poliza=EstadoPoliza.ACTIVA, cliente=cliente)
            return JsonResponse({'collection': [{'id': p.id, 'no_poliza': p.no_poliza}
                                                for p in polizas]}, encoder=Codec, safe=False)
        if 'contactos' in request.POST:
            poliza = Poliza.objects.get(id=request.POST.get('poliza'))
            contactos = ContactoAseguradora.objects.filter(aseguradora=poliza.aseguradora)
            return JsonResponse({'collection': [{'id': p.id, 'name': p.name}
                                                for p in contactos],
                                 'instance': poliza.to_json()}, encoder=Codec, safe=False)
        if 'calcular_tabla_pagos' in request.POST:
            instance = self.get_instance(request)
            data = tabla_cuotas(instance, request)
            return JsonResponse(data, safe=False, encoder=Codec)
        return super().post(request)

    def save_related(self, instance, data):
        for i in range(0, len(data.getlist('tabla_pagos_id'))):
            if data.getlist('tabla_pagos_id')[i] == '':
                p = Cuota(tramite=instance)
            else:
                p = Cuota.objects.get(id=int(data.getlist('tabla_pagos_id')[i]))
            p.numero = data.getlist('tabla_pagos_numero')[i]
            p.monto = data.getlist('tabla_pagos_monto')[i].replace(',', '')
            p.fecha_vence = parse_date(data.getlist('tabla_pagos_fecha_vence')[i])
            p.monto_comision = data.getlist('tabla_pagos_monto_comision')[i].replace(',', '')
            p.save()


# endregion


# region Aplicaciones


class ConfiguracionCotizador(Datatables):
    modal_width = 1200
    model = CotizadorConfig
    form = CotizadorConfigForm
    list_display = ('empresa.razon_social',)
    fieldsets = (
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('empresa', 'email_trust'),
                ('imagen',),
            )
        },
        {
            'id': 'auto',
            'name': 'Polizas de vehiculos',
            'fields': (
                ('aseguradora_automovil', 'ramo_automovil',),
                ('sub_ramo_automovil', 'tasa_automovil',),
                ('soa_automovil', 'porcentaje_deducible',),
                ('porcentaje_deducible_extencion_territorial', 'minimo_deducible',),
                ('soa_descuento',),
                ('email_cobranza', 'email_automovil'),
                ('fieldmap_automovil',),
            )
        },
        {
            'id': 'sepelio',
            'name': 'Polizas de sepelio',
            'fields': (
                ('aseguradora_sepelio', 'ramo_sepelio',),
                ('sub_ramo_sepelio', 'cliente_sepelio',),
                ('poliza_sepelio', 'poliza_sepelio_dependiente',),
                ('costo_sepelio', 'suma_sepelio',),
                ('email_sepelio',),
                ('fieldmap_sepelio',),
            )
        },
        {
            'id': 'accidente',
            'name': 'Polizas de accidentes',
            'fields': (
                ('aseguradora_accidente', 'ramo_accidente',),
                ('sub_ramo_accidente', 'cliente_accidente',),
                ('poliza_accidente', 'costo_accidente',),
                ('costo_carnet_accidente', 'suma_accidente',),
                ('suma_accidente_dependiente', 'email_accidente',),
                ('fieldmap_accidente',),
            )
        },
        {
            'id': 'vida',
            'name': 'Polizas de vida',
            'fields': (
                ('aseguradora_vida', 'ramo_vida',),
                ('sub_ramo_vida', 'cliente_vida',),
                ('poliza_vida', 'suma_vida',),
            )
        },
        {
            'id': 'email',
            'name': 'Correo de renovación',
            'fields': (
                ('email_renovacion',),
                ('email_cesion_derecho',),
                ('email_texto',),
            )
        },
    )

    def save_related(self, instance, data):
        for i in range(0, len(data.getlist('fieldmap'))):
            f = FieldMap.objects.get(id=data.getlist('fieldmap')[i])
            try:
                f.destiny_field = CampoAdicional.objects.get(id=data.getlist('destiny_field')[i])
            except:
                pass
            f.save()


# endregion


# region Usuarios


class Usuarios(Datatables):
    model = User
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username',)
    modal_width = 900
    form = UserForm

    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general del usuario',
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('lineas',),
            )
        },
    ]

    def get_queryset(self, filters, search_value):
        return super().get_queryset(filters, search_value).filter(is_staff=True)

    def save_related(self, instance, data):
        for line in Linea.objects.all():
            if str(line.id) in data.getlist('lineas'):
                LineaUser.objects.get_or_create(user=instance, linea=line)
            else:
                try:
                    LineaUser.objects.get(user=instance, linea=line).delete()
                except ObjectDoesNotExist:
                    pass

        super().save_related(instance, data)


class Roles(Datatables):
    model = Group
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)


# endregion


# region crm


class Oportunidades(Datatables):
    linea = None
    modal_width = 1400
    model = Oportunity
    form = OportunityForm
    list_display = ('code', 'prospect.name', 'vendedor.full_name',
                    ('Dias', 'dias'),
                    ('Etapa', 'status.name'),
                    'campain.name')
    search_fields = ('prospect__primer_nombre', 'prospect__segundo_nombre', 'prospect__cedula',
                     'prospect__apellido_paterno', 'prospect__apellido_materno', 'code',
                     'vendedor__first_name', 'vendedor__last_name')
    form_template = "trustseguros/lte/oportunity.html"
    list_template = "trustseguros/lte/oportunity-table.html"
    list_filter = ('campain', 'status')
    media = {
        'js': ['trustseguros/lte/js/municipio.js', ],
        'css': ('trustseguros/lte/css/oportunity-status.css',),
    }

    def get_queryset(self, filters, search_value):
        if self.linea:
            return super().get_queryset(filters, search_value).filter(linea=self.linea)
        return super().get_queryset(filters, search_value)

    def get(self, request, linea):
        self.linea = Linea.objects.get(id=linea)
        return super().get(request, import_form=ImportDataForm, linea=self.linea,
                           ramos_auto=SubRamo.objects.filter(show_quotation=True))

    def put(self, request, linea):
        self.linea = Linea.objects.get(id=linea)
        status = 203
        instance = self.model()
        form = self.get_form()(linea=self.linea)
        html_form = self.html_form(instance, request, form, 'PUT')
        errors = []

        if 'save' in request.PUT:
            instance, html_form, errors, status = self.process_request(request, 'PUT')
        return self.make_response(instance, html_form, errors, status)

    def post(self, request, linea):
        self.linea = Linea.objects.get(id=linea)

        if 'importar' in request.POST:
            extra_data = {}
            columns = request.POST.getlist('column')
            rows = len(request.POST.getlist(columns[0]))
            automovil = {
                'MARCA': 'marca',
                'MODELO': 'modelo',
                'ANIO': 'anno',
                'CHASIS': 'chasis'
            }
            prospect = {
                'cedula': request.POST.get('cedula', ''),
                'primer_nombre': request.POST.get('primer_nombre', ''),
                'segundo_nombre': request.POST.get('segundo_nombre', ''),
                'apellido_paterno': request.POST.get('apellido_paterno', ''),
                'apellido_materno': request.POST.get('apellido_materno', ''),
                'telefono': request.POST.get('telefono', ''),
                'celular': request.POST.get('celular', ''),
                'email_personal': request.POST.get('email_personal', ''),
                'domicilio': request.POST.get('domicilio', ''),
            }
            oportunity = {
                'no_poliza': request.POST.get('no_poliza', ''),
                'aseguradora': request.POST.get('aseguradora', ''),
                'fecha_vence': request.POST.get('fecha_vence', ''),
                'valor_nuevo': request.POST.get('valor_nuevo', ''),
                'rc_exceso': request.POST.get('rc_exceso', ''),
                'valor_exceso': request.POST.get('valor_exceso', ''),
            }
            form = ImportDataForm(request.POST)
            if form.is_valid():
                for n in range(0, rows):
                    p = None
                    cedula = request.POST.getlist(prospect['cedula'])[n]
                    if len(cedula) == 14:
                        try:
                            datos_vehiculo = {}
                            p, _ = Prospect.objects.get_or_create(cedula=cedula)
                            o = Oportunity()
                            o.prospect = p
                            for column in columns:
                                choice = request.POST.getlist("choice_" + column)[n]
                                value = request.POST.getlist(column)[n]
                                if choice and choice != '':
                                    if choice in prospect.keys():
                                        p.__setattr__(choice, value)

                                    if choice in oportunity.keys():
                                        if choice == 'fecha_vence':
                                            o.fecha_vence = timezone.datetime.strptime(value, '%d/%m/%Y')
                                        else:
                                            o.__setattr__(choice, value)

                                    if choice not in oportunity.keys() and choice not in prospect.keys():
                                        extra_data[choice] = value

                                    if choice in automovil.keys():
                                        datos_vehiculo[automovil[choice]] = value

                            p.save()
                            o.extra_data = json.dumps(extra_data)
                            o.linea = self.linea
                            o.campain = form.cleaned_data['campain']
                            o.ramo = form.cleaned_data['ramo']
                            o.sub_ramo = form.cleaned_data['sub_ramo']
                            o.vendedor = form.cleaned_data['vendedor']
                            if oportunity['valor_nuevo'] == '':
                                o.valor_nuevo = Referencia.valor_nuevo(datos_vehiculo).get('valor')
                            o.save()
                        except MultipleObjectsReturned:
                            print(f'error con la cedula {cedula}')
            return JsonResponse({})

        if 'print' in request.POST:
            return render_to_pdf_response(request,
                                          [f'trustseguros/lte/pdf/oportunity-{self.linea.id}.html',
                                           f'trustseguros/lte/pdf/oportunity.html',
                                           ],
                                          {
                                              'oportunity': Oportunity.objects.get(id=request.POST.get('id')),
                                              'today': timezone.now(),
                                          })

        if 'prepare_email' in request.POST:
            html = render_to_string([f'trustseguros/lte/includes/send-email-template-{self.linea.id}.html',
                                     f'trustseguros/lte/includes/send-email-template.html'],
                                    context={
                                        'oportunity': Oportunity.objects.get(id=request.POST.get('id')),
                                    },
                                    request=request)
            return JsonResponse({
                'html': html
            })

        if 'send_email' in request.POST:
            files = []
            cotizacion = render_to_pdf([f'trustseguros/lte/pdf/oportunity-{self.linea.id}.html',
                                        f'trustseguros/lte/pdf/oportunity.html', ], {
                                           'oportunity': Oportunity.objects.get(id=request.POST.get('oportunity_id'))
                                       })

            files.append(("attachment", ("Oferta.pdf", cotizacion)))

            send_email(request.POST.get('asunto'), request.POST.get('para'),
                       html=request.POST.get('email_content'), files=files, fr=request.POST.get('de'))
            return JsonResponse({})

        if 'prepare_register' in request.POST:
            html = render_to_string('trustseguros/lte/includes/ofertas.html',
                                    context={
                                        'oportunity': Oportunity.objects.get(id=request.POST.get('id')),
                                        'aseguradoras': Aseguradora.objects.all(),
                                    },
                                    request=request)
            return JsonResponse({
                'html': html
            })

        if 'calcular' in request.POST:
            return JsonResponse({
                'referencia': Referencia.valor_nuevo(request.POST)
            })

        if 'register' in request.POST:
            oportunity = Oportunity.objects.get(id=request.POST.get('oportunity').replace(',', ''))
            aseguradora = Aseguradora.objects.get(id=request.POST.get('aseguradora'))
            poliza = oportunity.registrar(aseguradora)
            return JsonResponse({
                'instance': poliza.to_json()
            }, encoder=Codec)

        return super().post(request)

    def save_related(self, instance, data):
        tipo_cliente = data.get('tipo_cliente', '1')
        try:
            if tipo_cliente == '1':
                prospect_form = ProspectForm(data,
                                             instance=Prospect.objects.get(
                                                 cedula=data.get('cedula')))
            if tipo_cliente == '2':
                prospect_form = ProspectForm(data,
                                             instance=Prospect.objects.get(
                                                 ruc=data.get('ruc')))
        except ObjectDoesNotExist:
            prospect_form = ProspectForm(data)
        if prospect_form.is_valid():
            prospect_form.save()
        else:
            print(prospect_form.errors)
        instance.prospect = prospect_form.instance
        instance.linea = self.linea
        instance.save()

        if 'cotizar' in data:
            for aseguradora in Aseguradora.objects.all():
                if str(aseguradora.id) in data.getlist('cotizacion'):
                    try:
                        cotizacion, _ = OportunityQuotation.objects.get_or_create(aseguradora=aseguradora,
                                                                                  oportunity=instance)
                        cotizacion.marca = data.get('MARCA')
                        cotizacion.modelo = data.get('MODELO')
                        cotizacion.anno = int(data.get('ANIO'))
                        try:
                            tarifa = Tarifa.objects.get(aseguradora=aseguradora, marca=cotizacion.marca,
                                                        modelo=cotizacion.modelo)
                            cotizacion.tarifa, cotizacion.coaseguro_robo, \
                            cotizacion.coaseguro_dano, cotizacion.deducible, \
                            cotizacion.exceso = tarifa.calcular_tarifa()
                        except ObjectDoesNotExist:
                            cotizacion.tarifa, cotizacion.coaseguro_robo, \
                            cotizacion.coaseguro_dano, cotizacion.deducible, \
                            cotizacion.exceso = aseguradora.calcular_tarifa()
                        cotizacion.emision = aseguradora.emision
                        cotizacion.suma_asegurada = cotizacion.get_suma_asegurada
                        cotizacion.prima = cotizacion.get_prima
                        cotizacion.total = cotizacion.prima_total
                        cotizacion.save()
                    except:
                        OportunityQuotation.objects.get(aseguradora=aseguradora,
                                                        oportunity=instance).delete()
                else:
                    try:
                        OportunityQuotation.objects.get(aseguradora=aseguradora,
                                                        oportunity=instance).delete()
                    except ObjectDoesNotExist:
                        pass

        if 'cambiar_status' in data:
            instance.status = int(data.get('siguiente_status'))
            instance.save()

        if not instance.linea.calcular_cotizacion:
            for idx, ida in enumerate(data.getlist('cotizacion')):
                cotizacion_aseguradora = Aseguradora.objects.get(id=ida)
                cotizacion_suma_asegurada = parse_float(data.getlist('cotizacion_suma_asegurada')[idx])
                cotizacion_deducible = parse_float(data.getlist('cotizacion_deducible')[idx])
                cotizacion_coaseguro_dano = parse_float(data.getlist('cotizacion_coaseguro_dano')[idx])
                cotizacion_coaseguro_robo = parse_float(data.getlist('cotizacion_coaseguro_robo')[idx])
                cotizacion_prima = parse_float(data.getlist('cotizacion_prima')[idx])
                oq, _ = OportunityQuotation.objects.get_or_create(
                    aseguradora=cotizacion_aseguradora,
                    oportunity=instance,
                )
                oq.marca = data.get('MARCA')
                oq.modelo = data.get('MODELO')
                try:
                    oq.anno = int(data.get('ANIO'))
                except:
                    pass
                oq.suma_asegurada = cotizacion_suma_asegurada
                oq.deducible = cotizacion_deducible
                oq.coaseguro_robo = cotizacion_coaseguro_dano
                oq.coaseguro_dano = cotizacion_coaseguro_robo
                oq.total = cotizacion_prima
                oq.save()

            for aseguradora in Aseguradora.objects.all():
                if not str(aseguradora.id) in data.getlist('cotizacion'):
                    try:
                        OportunityQuotation.objects.get(aseguradora=aseguradora,
                                                        oportunity=instance).delete()
                    except ObjectDoesNotExist:
                        pass


# endregion


# region cobranza


class Recibos(Datatables):
    modal_width = 1600
    model = Poliza
    form = ReciboForm
    form_template = "trustseguros/lte/recibo-modal.html"
    list_template = "trustseguros/lte/recibo-datatables.html"
    list_display = ('no_poliza', 'cliente.name', 'fecha_emision', 'fecha_vence', 'grupo.name', 'estado_poliza.label')
    search_fields = ('no_poliza', 'cliente__nombre')
    media = {
        'css': ['trustseguros/lte/css/recibo.fields.localize.css', ]
    }

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos de prima"
        model_name = "poliza"

    @staticmethod
    def get_status(cuota):
        if cuota.estado == EstadoPago.PAGADO:
            return cuota.estado
        today = datetime.now()
        if cuota.fecha_vence > today:
            return EstadoPago.VIGENTE
        else:
            return EstadoPago.VENCIDO

    def get_opts(self):
        return self.Meta

    def get_queryset(self, filters, search_value):
        return super().get_queryset(filters, search_value).filter(
            estado_poliza__in=[EstadoPoliza.ACTIVA, EstadoPoliza.CANCELADA])

    def get_buttons(self, request, instance):
        instance = self.get_instance(request)
        if instance.modificando_recibo:
            return [
                {
                    'class': 'btn btn-success btn-perform',
                    'perform': 'aplicar_cambio',
                    'callback': 'process_response',
                    'icon': 'fa fa-save',
                    'text': 'Guardar',
                },
            ]
        else:
            buttons = [
                {
                    'class': 'btn btn-warning btn-perform',
                    'perform': 'ecuenta',
                    'callback': 'imprimir_estado_cuenta',
                    'icon': 'fa fa-file-pdf',
                    'text': 'Estado de cuenta',
                },
                {
                    'class': 'btn btn-warning btn-perform',
                    'perform': 'modificar',
                    'callback': 'process_response',
                    'icon': 'fa fa-edit',
                    'text': 'Modificar',
                },
            ]
            if instance.recibo_editar:
                buttons.append({
                    'class': 'btn btn-danger btn-perform',
                    'perform': 'anular_recibo',
                    'callback': 'process_response',
                    'icon': 'fa fa-exclamation-triangle',
                    'text': 'Anular',
                })
            return buttons

    @staticmethod
    def opencuota(instance, request):
        fieldsets = (
            {'id': 'info',
             'name': 'Información de pago',
             'fields': (
                 ('nombre_cliente', 'numero_poliza', 'aseguradora', 'estado'),
                 ('numero_recibo', 'moneda', 'fecha_vence', 'dias_mora'),
                 ('monto', 'monto_pagado', 'saldo', 'monto_comision', 'comision_pagada', 'comision_pendiente'),
                 ('pagos',),
             )},
        )
        buttons = [{
            'class': 'btn btn-success btn-save-cuota',
            'icon': 'fa fa-save',
            'text': 'Guardar',
        }, ]
        return render_to_string('adminlte/datatables-modal.html',
                                context={'opts': Cuota._meta, 'fieldsets': fieldsets,
                                         'form': CuotaForm(instance=instance), 'instance': instance,
                                         'method': 'POST',
                                         'buttons': buttons},
                                request=request)

    def post(self, request):
        status = 200
        errors = []

        if 'cambiar_recibo' in request.POST:
            instance = self.get_instance(request)
            form = self.get_form()(request.POST, instance=instance)
            if form.is_valid():
                instance = self.get_instance(request)
                instance.recibo_editar = form.cleaned_data['recibo_editar']
                instance.save()
                form = self.get_form()(instance=instance)
            else:
                status = 203
                errors = self.get_form_errors(form)
            html_form = self.html_form(instance, request, form, 'POST')
            return self.make_response(instance, html_form, errors, status)

        if 'modificar' in request.POST:
            instance = self.get_instance(request)
            form = self.get_form()(request.POST, instance=instance)
            if form.is_valid():
                instance = self.get_instance(request)
                instance.modificando_recibo = True
                instance.save()
                form = self.get_form()(instance=instance)
            else:
                status = 203
                errors = self.get_form_errors(form)
            html_form = self.html_form(instance, request, form, 'POST')
            return self.make_response(instance, html_form, errors, status)

        if 'aplicar_cambio' in request.POST:
            instance = self.get_instance(request)
            form = self.get_form()(request.POST, instance=instance)
            if form.is_valid():
                instance = self.get_instance(request)
                instance.modificando_recibo = False
                if instance.recibo_editar:
                    recibo = instance.recibo_editar
                else:
                    recibo = instance
                recibo.subtotal = form.cleaned_data['subtotal']
                recibo.descuento = form.cleaned_data['descuento']
                recibo.emision = form.cleaned_data['emision']
                recibo.iva = form.cleaned_data['iva']
                recibo.otros = form.cleaned_data['otros']
                recibo.total = form.cleaned_data['total']
                recibo.per_comision = form.cleaned_data['per_comision']
                recibo.suma_asegurada = form.cleaned_data['suma_asegurada']
                recibo.amount_comision = form.cleaned_data['amount_comision']
                recibo.moneda = form.cleaned_data['moneda']
                recibo.f_pago = form.cleaned_data['f_pago']
                recibo.m_pago = form.cleaned_data['m_pago']
                recibo.cantidad_cuotas = form.cleaned_data['cantidad_cuotas']
                recibo.fecha_pago = form.cleaned_data['fecha_pago']
                recibo.save()
                instance.save()

                for i in range(0, len(request.POST.getlist('tabla_pagos_id'))):
                    if request.POST.getlist('tabla_pagos_id')[i] == '':
                        if instance.recibo_editar:
                            p = Cuota(tramite=recibo)
                        else:
                            p = Cuota(poliza=recibo)
                    else:
                        p = Cuota.objects.get(id=int(request.POST.getlist('tabla_pagos_id')[i]))
                    p.numero = request.POST.getlist('tabla_pagos_numero')[i]
                    p.monto = request.POST.getlist('tabla_pagos_monto')[i].replace(',', '')
                    p.monto_comision = request.POST.getlist('tabla_pagos_monto_comision')[i].replace(',', '')
                    p.fecha_vence = parse_date(request.POST.getlist('tabla_pagos_fecha_vence')[i])
                    p.estado = self.get_status(p)
                    p.save()

                form = self.get_form()(instance=instance)
            else:
                status = 203
                errors = self.get_form_errors(form)
            html_form = self.html_form(instance, request, form, 'POST')
            return self.make_response(instance, html_form, errors, status)

        if 'anular_recibo' in request.POST:
            instance = self.get_instance(request)
            form = self.get_form()(request.POST, instance=instance)
            if form.is_valid():
                instance = self.get_instance(request)
                if instance.recibo_editar:
                    recibo = instance.recibo_editar
                    recibo.genera_endoso = False
                    recibo.cuotas().delete()
                    recibo.save()
                    instance = self.get_instance(request)
                    form = self.get_form()(instance=instance)
            else:
                status = 203
                errors = self.get_form_errors(form)
            html_form = self.html_form(instance, request, form, 'POST')
            return self.make_response(instance, html_form, errors, status)

        if 'calcular_tabla_pagos' in request.POST:
            instance = self.get_instance(request)
            if instance.recibo_editar:
                instance = instance.recibo_editar
            data = tabla_cuotas(instance, request)
            return JsonResponse(data, safe=False, encoder=Codec)

        if 'opencuota' in request.POST:
            instance = Cuota.objects.get(id=request.POST.get('cuota'))
            return JsonResponse({
                'form': self.opencuota(instance, request), 'instance': instance.to_json()
            }, encoder=Codec)

        if 'guardarcuota' in request.POST:
            instance = Cuota.objects.get(id=request.POST.get('id'))
            form = CuotaForm(request.POST, instance=instance)
            if form.is_valid():
                for n, i in enumerate(request.POST.getlist('pagocuota')):
                    if i == '':
                        pago = PagoCuota(cuota=instance)
                    else:
                        pago = PagoCuota.objects.get(id=i)
                    pago.monto = request.POST.getlist('pagocuota-monto')[n]
                    pago.referencia_pago = request.POST.getlist('pagocuota-referencia_pago')[n]
                    pago.medio_pago = request.POST.getlist('pagocuota-medio_pago')[n]
                    pago.fecha_pago = parse_date(request.POST.getlist('pagocuota-fecha_pago')[n])
                    pago.fecha_pago_comision = parse_date(request.POST.getlist('pagocuota-fecha_pago_comision')[n])
                    pago.comision = request.POST.getlist('pagocuota-comision')[n]
                    pago.save()
                form.save()
                instance = form.instance
            return JsonResponse({
                'form': self.opencuota(instance, request), 'instance': instance.to_json()
            }, encoder=Codec)

        if 'nuevopago' in request.POST:
            html_form = render_to_string('trustseguros/lte/includes/nuevo-pago.html', {
                'form': PagoForm
            })
            return JsonResponse({
                'html': html_form
            }, encoder=Codec)

        if 'ecuenta' in request.POST:
            poliza = Poliza.objects.get(id=request.POST.get('id'))
            pages = []

            paginator = Paginator(poliza.estado_cuenta(), 14)

            for p in paginator.page_range:
                pages.append({
                    'page': p, 'range': len(paginator.page_range),
                    'registros': paginator.page(p)
                })
            return render_to_pdf_response(request, "trustseguros/lte/pdf/ecuenta.html", {
                'poliza': poliza,
                'pages': pages
            })

        return super().post(request)

    def save_related(self, instance, data):
        for i in range(0, len(data.getlist('tabla_pagos_id'))):
            if data.getlist('tabla_pagos_id')[i] == '':
                if instance.recibo_editar:
                    p = Cuota(tramite=instance.recibo_editar)
                else:
                    p = Cuota(poliza=instance)
            else:
                p = Cuota.objects.get(id=int(data.getlist('tabla_pagos_id')[i]))
            p.numero = data.getlist('tabla_pagos_numero')[i]
            p.monto = data.getlist('tabla_pagos_monto')[i].replace(',', '')
            p.fecha_vence = parse_date(data.getlist('tabla_pagos_fecha_vence')[i])
            p.monto_comision = data.getlist('tabla_pagos_monto_comision')[i].replace(',', '')
            p.save()


# endregion


# region siniestros


class SiniestroTramite(Datatables):
    modal_width = 1200
    model = SiniestroTramite
    form = SiniestroTramiteForm
    list_display = ('code', ('Cliente', 'cliente.name'),

                    ('Póliza', 'poliza.number'),
                    ('Tipo Movimiento', 'tipo_movimiento.name'),
                    ('Estado', 'estado.name'),
                    ('Siniestro Aseguradora', 'numero_siniestro'))
    fieldsets = [
        {
            'id': 'info',
            'name': 'Informacion general',
            'fields': (
                ('code', 'fecha_registro', 'fecha_suceso', 'estado'),
                ('cliente', 'poliza', 'ramo', 'sub_ramo'),
                ('grupo', 'tipo_asegurado', 'nombre_asegurado', 'contacto_aseguradora'),
                ('descripcion',),
            )
        },
        {
            'id': 'seguimiento',
            'name': 'Seguimiento',
            'fields': (
                ('fecha_envio_trust', 'fecha_recepcion_aseguradora', 'tramite_aseguradora', 'numero_siniestro'),
                ('tipo_movimiento', 'monto_reclamo', 'deducible', 'coaseguro'),
                ('gastos_presentados', 'no_cubierto'),
            )
        },
        {
            'id': 'drive',
            'name': 'Soportes',
            'fields': (
                ('drive',),
            )
        },
        {
            'id': 'bita',
            'name': 'Bitácora',
            'fields': (
                ('bitacora',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/js/siniestro.tramite.soportes.js', 'trustseguros/js/tramite.poliza.js',
               'trustseguros/js/siniestro.tramite.bitacora.js']
    }

    def post(self, request):
        if 'polizas' in request.POST:
            cliente = Cliente.objects.get(id=request.POST.get('cliente'))
            polizas = Poliza.objects.filter(estado_poliza=EstadoPoliza.ACTIVA, cliente=cliente)
            return JsonResponse({'collection': [{'id': p.id, 'no_poliza': p.no_poliza}
                                                for p in polizas]}, encoder=Codec, safe=False)
        if 'contactos' in request.POST:
            poliza = Poliza.objects.get(id=request.POST.get('poliza'))
            contactos = ContactoAseguradora.objects.filter(aseguradora=poliza.aseguradora)
            return JsonResponse({'collection': [{'id': p.id, 'name': p.name}
                                                for p in contactos],
                                 'instance': poliza.to_json()}, encoder=Codec, safe=False)

        return super().post(request)


class Siniestros(Datatables):
    modal_width = 1200
    model = Siniestro
    form = SiniestroForm
    list_display = ('reclamo_aseguradora', ('Cliente', 'cliente.name'),
                    ('Póliza', 'poliza.number'),
                    ('Estado', 'estado.name'))
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('reclamo_aseguradora', 'fecha_liquidacion', 'cliente', 'poliza'),
                ('ramo', 'sub_ramo', 'grupo', 'estado'),
                ('diagnostico',),
            )
        },
        {
            'id': 'seguimiento',
            'name': 'Seguimiento',
            'fields': (
                ('deducible_aplicado', 'deducible_pendiente', 'monto_pagado', 'forma_pago'),
                ('gastos_presentados', 'no_cubierto'),

            )
        },
        {
            'id': 'drive',
            'name': 'Soportes',
            'fields': (
                ('drive',),
            )
        },
        {
            'id': 'bita',
            'name': 'Bitácora',
            'fields': (
                ('bitacora',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/js/siniestro.soportes.js', 'trustseguros/js/tramite.poliza.js',
               'trustseguros/js/siniestro.bitacora.js']
    }

    def post(self, request):
        if 'polizas' in request.POST:
            cliente = Cliente.objects.get(id=request.POST.get('cliente'))
            polizas = Poliza.objects.filter(estado_poliza=EstadoPoliza.ACTIVA, cliente=cliente)
            return JsonResponse({'collection': [{'id': p.id, 'no_poliza': p.no_poliza}
                                                for p in polizas]}, encoder=Codec, safe=False)
        if 'contactos' in request.POST:
            poliza = Poliza.objects.get(id=request.POST.get('poliza'))
            contactos = ContactoAseguradora.objects.filter(aseguradora=poliza.aseguradora)
            return JsonResponse({'collection': [{'id': p.id, 'name': p.name}
                                                for p in contactos],
                                 'instance': poliza.to_json()}, encoder=Codec, safe=False)

        return super().post(request)


# endregion


# region reportes


class ReportLab(View):
    """
    Base class for all reports
    """
    form = None
    model = None
    filename = None

    @classmethod
    def as_view(cls, **initkwars):
        return login_required(super().as_view(**initkwars), login_url="/cotizador/login/")

    def get(self, request, **kwargs):
        return render(request, 'trustseguros/lte/reportes.html', {
            'form': self.form, 'filename': self.filename,
            **kwargs
        })

    @staticmethod
    def apply_filter(queryset, form_data):
        """
        :param queryset:
        :param form_data:
        :return: filtered queryset using form cleanead data
        """
        for filter_key in form_data.keys():
            if form_data.get(filter_key):
                queryset = queryset.filter(Q((filter_key, form_data.get(filter_key))))
        return queryset

    @staticmethod
    def to_json(instance):
        """
        :param instance:
        :return: return json object from instance data
        """
        return instance.to_json()

    def post(self, request, **kwargs):
        form = self.form(request.POST)
        raw_data = []
        if form.is_valid():
            queryset = self.model.objects.all()
            queryset = self.apply_filter(queryset, form.cleaned_data)
            for instance in queryset:
                raw_data.append(self.to_json(instance))
        return JsonResponse({'raw_data': raw_data}, encoder=Codec)


class ReportePoliza(ReportLab):
    """
    Base class for all póliza reports
    """
    model = Poliza
    form = ReportPolizaForm

    @staticmethod
    def to_json(instance):
        return {
            'Número Poliza': instance.no_poliza,
            'Fecha de registro': instance.created.strftime('%d/%m/%Y'),
            'Fecha Inicio': instance.fecha_emision.strftime('%d/%m/%Y'),
            'Fecha Fin': instance.fecha_vence.strftime('%d/%m/%Y'),
            'Ramo': get_attr(instance, 'ramo.name'),
            'Sub Ramo': get_attr(instance, 'sub_ramo.name'),
            'Aseguradora': get_attr(instance, 'aseguradora.name'),
            'Cliente': get_attr(instance, 'cliente.full_name'),
            'Contratante': get_attr(instance, 'contratante.full_name'),
            'Grupo': get_attr(instance, 'grupo.name'),
            'Estado': instance.get_estado_poliza_display(),
            'Prima': get_attr(instance, 'prima_neta'),
        }


class ReportePolizaEmitida(ReportePoliza):
    filename = "Reporte de pólizas emitidas.xlsx"


class ReportePolizaCancelada(ReportePoliza):
    filename = "Reporte de pólizas canceladas.xlsx"

    @staticmethod
    def apply_filter(queryset, form_data):
        queryset = queryset.filter(estado_poliza=EstadoPoliza.CANCELADA)
        return ReportLab.apply_filter(queryset, form_data)

    @staticmethod
    def to_json(instance):
        def cancelacion(i):
            if i.fecha_cancelacion:
                return i.fecha_cancelacion.strftime('%d/%m/%Y')
            else:
                return ''

        return {
            'Número Poliza': instance.no_poliza,
            'Fecha de registro': instance.created.strftime('%d/%m/%Y'),
            'Fecha Inicio': instance.fecha_emision.strftime('%d/%m/%Y'),
            'Fecha Fin': instance.fecha_vence.strftime('%d/%m/%Y'),
            'Fecha Cancelación': cancelacion(instance),
            'Motivo Cancelación': instance.get_motivo_cancelacion_display(),
            'Ramo': instance.ramo.name,
            'Sub Ramo': instance.sub_ramo.name,
            'Aseguradora': get_attr(instance, 'aseguradora.name'),
            'Cliente': instance.cliente.full_name,
            'Contratante': instance.contratante.full_name,
            'Grupo': instance.grupo.name,
            'Estado': instance.get_estado_poliza_display(),
            'Prima': instance.prima_neta,
        }


class ReportePolizaRenovada(ReportePoliza):
    model = Poliza
    form = ReportPolizaForm
    filename = "Reporte de pólizas renovadas.xlsx"

    @staticmethod
    def apply_filter(queryset, form_data):
        queryset = queryset.filter(estado_poliza=EstadoPoliza.RENOVADA)
        return ReportLab.apply_filter(queryset, form_data)


class ReportePolizaPorVencer(ReportePoliza):
    filename = "Reporte de pólizas por vencer.xlsx"
    form = ReportPolizaVencerForm

    @staticmethod
    def apply_filter(queryset, form_data):
        queryset = queryset.filter(estado_poliza__in=[EstadoPoliza.PENDIENTE,
                                                      EstadoPoliza.ACTIVA])
        return ReportLab.apply_filter(queryset, form_data)


class ReporteTramite(ReportLab):
    model = Tramite
    form = ReportTramiteForm
    filename = "Reporte de trámites.xlsx"

    @staticmethod
    def to_json(instance):
        o = {
            'Número de trámite': instance.code,
            'Tipo de trámite': instance.get_tipo_tramite_display(),
            'Fecha de registro': instance.created.strftime('%d/%m/%Y'),
            'Ingresado por': instance.user.username,
            'Estado': instance.get_estado_display(),
        }
        if instance.cliente:
            o['Cliente'] = instance.cliente.nombre
        if instance.poliza:
            o['Poliza'] = instance.poliza.code
        o['Duracion'] = str(instance.duracion()) + " dias"
        return o


class ReporteCRM(ReportLab):
    model = Oportunity
    form = ReporteCrmForm
    filename = "Reporte de oportunidades de negocio.xlsx"

    @staticmethod
    def to_json(instance):
        def vencimiento(i):
            if i.fecha_vence:
                return i.fecha_vence.strftime('%d/%m/%Y')
            else:
                return None

        return {
            'Número': get_attr(instance, 'code'),
            'Línea': get_attr(instance, 'linea.name'),
            'Campaña': get_attr(instance, 'campain.name'),
            'Prospecto': get_attr(instance, 'prospect.get_full_name'),
            'Ramo': get_attr(instance, 'ramo.name'),
            'Sub Ramo': get_attr(instance, 'sub_ramo.name'),
            'Estado': instance.get_status_display(),
            'Vendedor': get_attr(instance, 'vendedor.username'),
            'Póliza': get_attr(instance, 'no_poliza'),
            'Aseguradora': get_attr(instance, 'aseguradora.name'),
            'Fecha de vencimiento': vencimiento(instance),
            'Valor nuevo': get_attr(instance, 'valor_nuevo'),
            'Monto exceso': get_attr(instance, 'valor_exceso'),
            'Razón no concretada la venta': instance.get_causal_display(),
        }


class ReporteCotizaciones(ReportLab):
    model = Oportunity
    form = ReporteCrmForm
    filename = "Reporte de cotizaciones.xlsx"

    @staticmethod
    def quotation(instance, aseguradora):
        try:
            quotation = OportunityQuotation.objects.get(oportunity=instance, aseguradora=aseguradora)
            return {
                f'Suma asegurada {aseguradora.name}': quotation.suma_asegurada,
                f'Deducible {aseguradora.name}': quotation.deducible,
                f'Coaseguro robo {aseguradora.name}': quotation.coaseguro_robo,
                f'Coaseguro daños {aseguradora.name}': quotation.coaseguro_dano,
                f'Prima total {aseguradora.name}': quotation.prima_total,
            }
        except ObjectDoesNotExist:
            return {
                f'Suma asegurada {aseguradora.name}': '',
                f'Deducible {aseguradora.name}': '',
                f'Coaseguro robo {aseguradora.name}': '',
                f'Coaseguro daños {aseguradora.name}': '',
                f'Prima total {aseguradora.name}': '',
            }

    def to_json(self, instance):
        obj = {
            'Prospecto': get_attr(instance, 'prospect.get_full_name'),
            'Marca': instance.data_load().get('MARCA', None),
            'Modelo': instance.data_load().get('MODELO', None),
            'Año': instance.data_load().get('ANIO', None),
            'Chasis': instance.data_load().get('CHASIS', None),
            'Motor': instance.data_load().get('MOTOR', None),
            'Placa': instance.data_load().get('PLACA', None),
        }
        for aseguradora in Aseguradora.objects.filter(active=True).order_by('name'):
            quote = self.quotation(instance, aseguradora)
            obj = {**obj, **quote}
        return obj


class ReporteSiniestro(ReportLab):
    model = Siniestro
    form = ReporteSiniestroForm
    filename = "Reporte de siniestros.xlsx"


class ReporteMora(ReportLab):
    model = Poliza
    form = ReporteCarteraForm
    filename = "Reporte de mora.xlsx"

    @staticmethod
    def apply_filter(queryset, form_data):
        return queryset

    @staticmethod
    def to_json(instance, date):
        return {
            'Grupo': get_attr(instance, 'grupo.name'),
            'Ramo': get_attr(instance, 'ramo.name'),
            'Sub ramo': get_attr(instance, 'sub_ramo.name'),
            'Contratante': get_attr(instance, 'contratante'),
            'Asegurado': get_attr(instance, 'cliente.full_name'),
            'Número Tel': get_attr(instance, 'cliente.celular'),
            'Correo electrónico': get_attr(instance, 'cliente.email_personal'),
            'Póliza': get_attr(instance, 'no_poliza'),
            'Compañía': get_attr(instance, 'aseguradora.name'),
            'Recibo de prima': get_attr(instance, 'no_recibo'),
            'Moneda': get_attr(instance, 'moneda'),
            'Fecha emision': get_attr(instance, 'fecha_emision'),
            'Fecha vence': get_attr(instance, 'fecha_vence'),
            'Día de Cobro': get_attr(instance, 'fecha_pago'),
            'Forma de pago': instance.get_f_pago_display(),
            'Medio de pago': instance.get_m_pago_display(),
            'Total': get_attr(instance, 'prima_total'),
            'Pagado': get_attr(instance, 'total_pagado'),
            'Pendiente': get_attr(instance, 'saldo_pendiente'),
            'Corriente': instance.saldo_corriente(date),
            '1 – 30': instance.saldo_mora_dias(date, 0, 30),
            '31 – 60': instance.saldo_mora_dias(date, 30, 60),
            '61 – 90': instance.saldo_mora_dias(date, 60, 90),
            '91 – 120': instance.saldo_mora_dias(date, 90, 120),
            'Más de 120': instance.saldo_mora_end(date, 120),
            'Total venc.': instance.saldo_vencido(date),
        }

    def post(self, request, **kwargs):
        form = self.form(request.POST)
        raw_data = []
        if form.is_valid():
            queryset = self.model.objects.all()
            queryset = self.apply_filter(queryset, form.cleaned_data)
            for instance in queryset:
                raw_data.append(self.to_json(instance, form.cleaned_data['date']))
        return JsonResponse({'raw_data': raw_data}, encoder=Codec)


class ReporteComision(ReportLab):
    model = PagoCuota
    form = ReporteComisionForm
    filename = "Reporte de comisión.xlsx"

    @staticmethod
    def to_json(instance):
        return {
            'Contratante': get_attr(instance, 'get_poliza.contratante'),
            'Cliente': get_attr(instance, 'get_poliza.cliente'),
            'Ramo': get_attr(instance, 'get_poliza.ramo'),
            'Póliza': get_attr(instance, 'get_poliza.no_poliza'),
            'Aseguradora': get_attr(instance, 'get_poliza.aseguradora'),
            'Fecha de inicio': get_attr(instance, 'get_poliza.fecha_emision'),
            'Fecha de vencimiento': get_attr(instance, 'get_poliza.fecha_vence'),
            'Concepto': get_attr(instance, 'get_poliza.get_concepto_display'),
            'Número de recibo': get_attr(instance, 'cuota.get_recibo'),
            'Moneda': get_attr(instance, 'get_poliza.moneda'),
            'Monto': get_attr(instance, 'monto'),
            'Comisión': get_attr(instance, 'comision'),
            'Fecha de pago': get_attr(instance, 'fecha_pago'),
            'Fecha de pago comisión': get_attr(instance, 'fecha_pago_comision'),
            'Referencia de pago': get_attr(instance, 'referencia_pago'),
            'Medio de pago': get_attr(instance, 'get_medio_pago_display'),
            'Número de cuota': get_attr(instance, 'cuota.numero'),
            '2% IR': get_attr(instance, 'ir'),
            '% Alcaldía': get_attr(instance, 'alcaldia'),
            'Comisión recibida': get_attr(instance, 'comision_deducida'),
        }

# endregion
