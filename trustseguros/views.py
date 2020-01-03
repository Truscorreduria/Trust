from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import *
from django.http import JsonResponse
from grappelli_extras.utils import Codec
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from django.contrib import messages
import numpy as np
from django.views.generic import View
import os
from django.conf import settings
from django.shortcuts import Http404, HttpResponse
from django.forms import modelform_factory
from django.contrib.admin.utils import flatten
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from functools import reduce
import operator


@staff_member_required
def documentos(request):
    if request.method == "GET":
        files = []
        try:
            type = ContentType.objects.get(app_label=request.GET.get('app_label'),
                                           model=request.GET.get('model'))
            original = type.get_object_for_this_type(id=int(request.GET.get('id')))
        except:
            original = None
            type = None
        if original:
            files = Archivo.objects.filter(type=type, key=original.id)
        return render(request, 'trustseguros/documentos_adjuntos.html',
                      {'archivos': files, 'catalogos': catalogoArchivo.objects.all().order_by('nombre'),
                       'original': original.to_json()})

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
                file = Archivo()
                document = request.FILES['file']
                file.nombre = document.name
                file.catalogo = request.POST.get('catalogo')
                file.fecha_caducidad = request.POST.get('fecha_caducidad')
                file.archivo = document
                file.type = type
                file.key = original.id
                file.save()
                print(file)
            return render(request, 'trustseguros/include/row_document.html', {
                'archivo': file.to_json(), 'catalogos': catalogoArchivo.objects.all().order_by('nombre')
            })
        if 'update' in request.POST:
            print(request.POST)
            a = Archivo.objects.get(id=int(request.POST.get('id')))
            a.nombre = request.POST.get('nombre')

            try:
                a.catalogo = catalogoArchivo.objects.get(id=int(request.POST.get('catalogo')))
            except:
                pass

            try:
                a.fecha_caducidad = request.POST.get('fecha')
            except:
                pass

            a.save()
            return JsonResponse(a.to_json(), encoder=Codec)
        if 'delete' in request.POST:
            Archivo.objects.get(id=int(request.POST.get('id'))).delete()
            return JsonResponse({})


@staff_member_required
def certificados(request):
    return render(request, 'trustseguros/include/certificados.html', {
        'poliza': Poliza.objects.get(id=int(request.GET.get('poliza'))),
        'form': CertificadoForm()
    })


@staff_member_required
def certificado(request):
    try:
        print(request.POST.get('id'))
        instance = get_object_or_404(Certificado, id=int(request.POST.get('id')))
    except:
        print("no instance")
        instance = None
    form = CertificadoForm(request.POST or None, instance=instance)
    print(form.is_valid())
    if form.is_valid():
        cert = form.save()
        return JsonResponse(cert.to_json(), encoder=Codec)
    else:
        print(form.errors)
        return JsonResponse({}, encoder=Codec)


# region importacion de datos

def format_date(value):
    return value


def try_import(obj, prop, source, value, iter, is_date=False):
    try:
        if not source[value][iter] or source[value][iter] == 'nan' or source[value][iter] == '-' or source[value][
            iter] == '.':
            obj[prop] = None
        else:
            if is_date:
                print(format_date(source[value][iter]))
                obj[prop] = format_date(source[value][iter])
            obj[prop] = source[value][iter]
    except:
        pass


def smart_key(options, value):
    for obj in options:
        if obj[1] == value:
            return obj[0]
    return None


def get_aseguradora(name):
    a, _ = Aseguradora.objects.get_or_create(nombre=name)
    return a


def get_ramo(name):
    r, _ = Ramo.objects.get_or_create(nombre=name)
    return r


def get_subramo(name, ramo):
    r = get_ramo(ramo)
    r.save()
    sr, _ = SubRamo.objects.get_or_create(nombre=name, ramo=r)
    sr.save()
    return sr


def get_cliente(tipo, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, genero, tipo_identificacion,
                numero_identificacion, vecimiento_documento, fecha_nacimiento, estado_civil, ocupacion,
                razon_social, ruc, fecha_expedicion, fecha_constitucion, actividad_economica):
    if smart_key(TIPOS_CLIENTE, tipo) == Cliente.NATURAL:
        c, _ = Cliente.objects.get_or_create(tipo=Cliente.NATURAL,
                                             tipo_identificacion=smart_key(
                                                 Cliente.TIPOS_IDENTIFICACION, tipo_identificacion),
                                             numero_identificacion=numero_identificacion)
        c.genero = smart_key(Cliente.GENEROS, genero)
        c.primer_nombre = primer_nombre
        c.segundo_nombre = segundo_nombre
        c.primer_apellido = primer_apellido
        c.segundo_apellido = segundo_apellido
        c.vecimiento_documento = vecimiento_documento
        c.fecha_nacimiento = fecha_nacimiento
        c.estado_civil = estado_civil
        c.ocupacion = ocupacion
        c.save()
        return c
    if smart_key(TIPOS_CLIENTE, tipo) == Cliente.JURIDICO:
        c, _ = Cliente.objects.get_or_create(tipo=Cliente.JURIDICO,
                                             ruc=ruc)
        c.razon_social = razon_social
        c.fecha_expedicion = format_date(fecha_expedicion)
        c.fecha_constitucion = format_date(fecha_constitucion)
        c.actividad_economica = actividad_economica
        c.save()
        return c


def get_vendedor(name):
    v, _ = Vendedor.objects.get_or_create(nombre=name)
    return v


def importar_polizas(request):
    data = pd.read_excel(request.FILES['file'])
    data = data.replace(np.nan, '')
    dict_data = data.to_dict('index')
    success = []
    for n in range(0, len(data['numero_poliza'])):
        o = dict_data[n]
        form = ImportPolizaForm(o)
        if form.is_valid():
            form.save()
            success.append(form.instance)
        else:
            err_values = list(form.errors.values())
            err = "Línea # " + str(n + 2)
            for nn, e in enumerate(list(form.errors.keys())):
                err += " %s %s" % (e, " ".join(err_values[nn]))
            err += " Esta linea no se importó!"
            messages.error(request, err)

    messages.success(request, "%s empresas polizas con éxito." % len(success))
    return JsonResponse({}, encoder=Codec)


class ImportMixin:
    title = ""
    import_template = ""
    form = None
    template = ""

    def _to_dict(self, qdict):
        return {k: v for k, v in qdict.lists()}

    def get_fields(self):
        return self.form().fields

    def dtypes(self):
        return {field: str for field in self.get_fields()}

    def get(self, request):
        return render(request, "trustseguros/admin/import.html", {
            'title': self.title, 'forms': [], 'fields': self.get_fields(),
            'form': self.form, 'template': self.template
        })


class ImportCompany(View, ImportMixin):
    title = "Importar clientes jurídicos"
    form = ImportEmpresaForm
    template = "cliente_juridico.xlsx"

    def post(self, request):
        form_list = []
        error_list = []
        if 'apply' in request.POST:
            data = self._to_dict(request.POST)
            print(data)
            del data['csrfmiddlewaretoken']
            del data['apply']
            for n, t in enumerate(data['tipo']):
                o = dict()
                for field in data.keys():
                    try:
                        o[field] = data[field][n]
                    except:
                        print(data[field])
                form = self.form(o)
                if form.is_valid():
                    form.save()
                    form_list.append(form)
                else:
                    error_list.append(form)
            messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
            if len(error_list) > 0:
                messages.error(request, "%s empresas produjeron error!" % len(error_list))
                return render(request, "trustseguros/admin/import.html", {
                    'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
                    'form': self.form, 'template': self.template
                })
            return HttpResponseRedirect('/admin/trustseguros/cliente/')
        else:
            data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
            data = data.replace(np.nan, '')
            dict_data = data.to_dict('index')
            for n in range(0, len(data['razon_social'])):
                o = dict_data[n]
                o['tipo'] = 2
                form = self.form(o)
                form.is_valid()
                form_list.append(form)
        return render(request, "trustseguros/admin/import-table.html", {
            'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
        })


class ImportPerson(View, ImportMixin):
    title = "Importar personas naturales"
    form = ImportPersonaForm
    template = "cliente_natural.xlsx"

    def post(self, request):
        form_list = []
        error_list = []
        if 'apply' in request.POST:
            data = self._to_dict(request.POST)
            print(data)
            del data['csrfmiddlewaretoken']
            del data['apply']
            for n, t in enumerate(data['tipo']):
                o = dict()
                for field in data.keys():
                    try:
                        o[field] = data[field][n]
                    except:
                        print(data[field])
                form = self.form(o)
                if form.is_valid():
                    form.save()
                    form_list.append(form)
                else:
                    error_list.append(form)
            messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
            if len(error_list) > 0:
                messages.error(request, "%s empresas produjeron error!" % len(error_list))
                return render(request, "trustseguros/admin/import.html", {
                    'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
                    'form': self.form
                })
            return HttpResponseRedirect('/admin/trustseguros/cliente/')
        else:
            data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
            data = data.replace(np.nan, '')
            dict_data = data.to_dict('index')
            for n in range(0, len(data['primer_nombre'])):
                o = dict_data[n]
                o['tipo'] = 1
                form = self.form(o)
                form.is_valid()
                form_list.append(form)
        return render(request, "trustseguros/admin/import-table.html", {
            'forms': form_list, 'form': self.form, 'fields': self.get_fields()
        })


class ImportPoliza(View, ImportMixin):
    title = "Importar pólizas"
    form = ImportPolizaForm
    template = "poliza.xlsx"

    def post(self, request):
        form_list = []
        error_list = []
        if 'apply' in request.POST:
            data = self._to_dict(request.POST)
            print(data)
            del data['csrfmiddlewaretoken']
            del data['apply']
            for n, t in enumerate(data['numero_poliza']):
                o = dict()
                for field in data.keys():
                    try:
                        o[field] = data[field][n]
                    except:
                        print(data[field])
                form = self.form(o)
                if form.is_valid():
                    form.save()
                    form_list.append(form)
                else:
                    error_list.append(form)
            messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
            if len(error_list) > 0:
                messages.error(request, "%s empresas produjeron error!" % len(error_list))
                return render(request, "trustseguros/admin/import.html", {
                    'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
                    'form': self.form, 'template': self.template
                })
            return HttpResponseRedirect('/admin/trustseguros/poliza/')
        else:
            data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
            data = data.replace(np.nan, '')
            dict_data = data.to_dict('index')
            for n in range(0, len(data['numero_poliza'])):
                o = dict_data[n]
                form = self.form(o)
                form.is_valid()
                form_list.append(form)
        return render(request, "trustseguros/admin/import-table.html", {
            'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
        })


class ImportCertificadoEdificio(View, ImportMixin):
    title = "Importar certificados de edificios"
    form = ImportCertificadoEdificioForm
    template = "certificado_edificio.xlsx"

    def post(self, request):
        form_list = []
        error_list = []
        if 'apply' in request.POST:
            data = self._to_dict(request.POST)
            del data['csrfmiddlewaretoken']
            del data['apply']
            for n, t in enumerate(data['numero_poliza']):
                o = dict()
                for field in data.keys():
                    try:
                        o[field] = data[field][n]
                    except:
                        print(data[field])
                form = self.form(o)
                if form.is_valid():
                    form.save()
                    form_list.append(form)
                else:
                    error_list.append(form)
            messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
            if len(error_list) > 0:
                messages.error(request, "%s empresas produjeron error!" % len(error_list))
                return render(request, "trustseguros/admin/import.html", {
                    'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
                    'form': self.form, 'template': self.template
                })
            return HttpResponseRedirect('/admin/trustseguros/certificado/')
        else:
            data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
            data = data.replace(np.nan, '')
            dict_data = data.to_dict('index')
            for n in range(0, len(data['numero_poliza'])):
                o = dict_data[n]
                o['tipo'] = 'edificio'
                form = self.form(o)
                form.is_valid()
                form_list.append(form)
        return render(request, "trustseguros/admin/import-table.html", {
            'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
        })


class ImportCertificadoAuto(View, ImportMixin):
    title = "Importar certificados de autos"
    form = ImportCertificadoAutoForm
    template = "certificado_auto.xlsx"

    def post(self, request):
        form_list = []
        error_list = []
        if 'apply' in request.POST:
            data = self._to_dict(request.POST)
            print(data)
            del data['csrfmiddlewaretoken']
            del data['apply']
            for n, t in enumerate(data['numero_poliza']):
                o = dict()
                for field in data.keys():
                    try:
                        o[field] = data[field][n]
                    except:
                        print(data[field])
                form = self.form(o)
                if form.is_valid():
                    form.save()
                    form_list.append(form)
                else:
                    error_list.append(form)
            messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
            if len(error_list) > 0:
                messages.error(request, "%s empresas produjeron error!" % len(error_list))
                return render(request, "trustseguros/admin/import.html", {
                    'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
                    'form': self.form, 'template': self.template
                })
            return HttpResponseRedirect('/admin/trustseguros/certificado/')
        else:
            data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
            data = data.replace(np.nan, '')
            dict_data = data.to_dict('index')
            for n in range(0, len(data['numero_poliza'])):
                o = dict_data[n]
                o['tipo'] = 'auto'
                form = self.form(o)
                form.is_valid()
                form_list.append(form)
        return render(request, "trustseguros/admin/import-table.html", {
            'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
        })


class ImportCertificadoPersona(View, ImportMixin):
    title = "Importar certificados de personas"
    form = ImportCertificadoPersonaForm
    template = "certificado_persona.xlsx"

    def post(self, request):
        form_list = []
        error_list = []
        if 'apply' in request.POST:
            data = self._to_dict(request.POST)
            print(data)
            del data['csrfmiddlewaretoken']
            del data['apply']
            for n, t in enumerate(data['numero_poliza']):
                o = dict()
                for field in data.keys():
                    try:
                        o[field] = data[field][n]
                    except:
                        print(data[field])
                form = self.form(o)
                if form.is_valid():
                    form.save()
                    form_list.append(form)
                else:
                    error_list.append(form)
            messages.success(request, "%s empresas se importaron con éxito!" % len(form_list))
            if len(error_list) > 0:
                messages.error(request, "%s empresas produjeron error!" % len(error_list))
                return render(request, "trustseguros/admin/import.html", {
                    'title': self.title, 'forms': error_list, 'fields': self.get_fields(),
                    'form': self.form, 'template': self.template
                })
            return HttpResponseRedirect('/admin/trustseguros/certificado/')
        else:
            data = pd.read_excel(request.FILES['file'], dtype=self.dtypes())
            data = data.replace(np.nan, '')
            dict_data = data.to_dict('index')
            for n in range(0, len(data['numero_poliza'])):
                o = dict_data[n]
                o['tipo'] = 'persona'
                form = self.form(o)
                form.is_valid()
                form_list.append(form)
        return render(request, "trustseguros/admin/import-table.html", {
            'forms': form_list, 'form': self.form, 'fields': self.get_fields(), 'template': self.template
        })


def download(request):
    file_name = request.POST.get('file_name', request.GET.get('file_name'))
    path_to_file = os.path.join(settings.STATIC_ROOT, 'descargas', file_name)
    if os.path.exists(path_to_file):
        with open(path_to_file, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(file_name)
            response['X-Sendfile'] = path_to_file
            return response
    else:
        raise Http404


# endregion


# region lte

def index(request):
    return render(request, 'trustseguros/lte/index.html', {

    })


class Datatables(View):
    modal_width = 600
    list_template = "trustseguros/lte/datatables.html"
    form_template = "trustseguros/lte/datatables-modal.html"
    model = None
    form = None
    fieldsets = None
    fields = None
    media = None
    list_display = ()
    search_fields = ()

    def get_fields(self):
        field_names = []
        if self.fieldsets:
            for fieldset in self.fieldsets:
                field_names.extend(flatten(fieldset['fields']))
        elif self.fields:
            return self.fields
        return field_names

    def get_form(self):
        if not self.form:
            return modelform_factory(self.model, fields=self.get_fields())
        else:
            return self.form

    def html_form(self, instance, request, form):
        return render_to_string(self.form_template,
                                context={'opts': self.model._meta, 'fieldsets': self.fieldsets,
                                         'form': form, 'instance': instance},
                                request=request)

    def get(self, request):
        return render(request, self.list_template, {
            'opts': self.model._meta, 'list_display': self.list_display,
            'form': self.get_form(), 'form_template': self.form_template,
            'modal_width': self.modal_width, 'media': self.media
        })

    def save_related(self, instance, data):
        pass

    def get_filters(self, search_value):
        return [Q(('{}__icontains'.format(field), search_value)) for field in self.search_fields]

    def get_queryset(self, search_value):
        queryset = self.model.objects.all()
        if search_value:
            queryset = self.model.objects.filter(reduce(operator.or_, self.get_filters(search_value)))
        return queryset

    def get_ordered_queryset(self, search_value, order):
        queryset = self.get_queryset(search_value)
        return queryset.order_by(order)

    def get_data(self, start, per_page, search_value, draw, order=None):
        queryset = self.get_queryset(search_value)
        if order:
            queryset = self.get_ordered_queryset(search_value, order)
        page = int(start / per_page) + 1
        paginator = Paginator(queryset, per_page)
        data = [x.to_json() for x in paginator.page(page).object_list]
        return {
            'draw': draw,
            'data': data,
            'recordsTotal': len(data),
            'recordsFiltered': queryset.count(),
        }

    def post(self, request):
        print(request.POST)
        status = 200
        errors = []
        instance = None

        if 'list' in request.POST:
            order = None
            start = int(request.POST.get('start', 0))
            draw = int(request.POST.get('draw', 0))
            per_page = int(request.POST.get('length', 10))
            search_value = request.POST.get('search[value]', None)

            order_column = request.POST.get('order[0][column]', None)
            order_dir = request.POST.get('order[0][dir]', None)

            if order_column and order_dir:
                order = ''
                if order_dir == 'desc':
                    order += '-'
                order += self.list_display[int(order_column)].split('.')[0]

            return JsonResponse(self.get_data(start, per_page, search_value, draw, order), encoder=Codec)
        if 'open' in request.POST:
            instance = self.model.objects.get(id=int(request.POST.get('id')))
            form = self.get_form()(instance=instance)
            html_form = self.html_form(instance, request, form)
        if 'save' in request.POST:
            instance = self.model.objects.get(id=int(request.POST.get('id')))
            form = self.get_form()(request.POST, instance=instance)
            html_form = self.html_form(instance, request, form)
            if form.is_valid():
                form.save()
                instance = form.instance
                self.save_related(instance=instance, data=request.POST)
            else:
                errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                status = 203

        return JsonResponse({'instance': instance.to_json(),
                             'form': html_form, 'errors': errors}, encoder=Codec,
                            status=status)

    def put(self, request):
        status = 203
        instance = self.model()
        form = self.get_form()()
        html_form = self.html_form(instance, request, form)
        errors = []

        if 'save' in request.PUT:
            try:
                form = self.get_form()(request.PUT)
                if form.is_valid():
                    form.save()
                    instance = form.instance
                    status = 200
                    self.save_related(instance=instance, data=request.PUT)
                else:
                    errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                    html_form = self.html_form(instance, request, form)
            except IntegrityError as e:
                print(e)
                # errors.append(dict(e))

        return JsonResponse({'instance': instance.to_json(), 'form': html_form,
                             'errors': errors}, status=status)


class Aseguradoras(Datatables):
    modal_width = 900
    model = Aseguradora
    list_display = ('nombre', 'ruc', 'email', 'telefono', 'direccion')
    search_fields = ('nombre', 'ruc', 'email', 'telefono', 'departamento', 'municipio', 'direccion', 'cuenta_bancaria')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('nombre', 'ruc'),
                ('email', 'telefono'),
                ('departamento', 'municipio', 'cuenta_bancaria'),
                ('direccion',),
            )
        },
    ]

    media = {
        'js': ['trustseguros/lte/js/municipio.js',]
    }


class ClientesNaturales(Datatables):
    modal_width = 900
    model = ClienteNatural
    list_display = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'numero_identificacion',
                    'departamento.name', 'municipio.name')
    search_fields = ('numero_identificacion', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información General',
            'fields': (
                ('primer_nombre', 'segundo_nombre'),
                ('primer_apellido', 'segundo_apellido'),
                ('tipo_identificacion', 'numero_identificacion'),
                ('telefono', 'celular'),
                ('departamento', 'municipio'),
                ('direccion',),
            )
        }
    ]

    media = {
        'js': ['trustseguros/lte/js/municipio.js',]
    }


class ClientesJuridicos(Datatables):
    modal_width = 900
    model = ClienteJuridico
    list_display = ('numero_identificacion', 'razon_social', 'fecha_constitucion', 'actividad_economica', 'pagina_web',
                    'observaciones')
    search_fields = ('numero_identificacion', 'tipo_identificacion')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información General',
            'fields': (
                ('numero_identificacion', 'razon_social'),
                ('fecha_constitucion', 'actividad_economica'),
                ('departamento', 'municipio'),
                ('pagina_web',),
                ('observaciones',),
            )
        }
    ]

    media = {
        'js': ['trustseguros/lte/js/municipio.js',]
    }


class Polizas(Datatables):
    modal_width = 900
    model = Poliza
    list_display = (
        'numero_poliza', 'cliente.full_name', 'aseguradora.nombre', 'sub_ramo.nombre', 'fecha_expedicion',
        'fecha_inicio',
        'fecha_fin')

    form = LtePolizaForm

    fieldsets = [
        {'id': 'info', 'name': 'Información General',
         'fields': (
             ('cliente',),
             ('aseguradora', 'tipo'),
             ('sub_ramo', 'vendedor'),
             ('numero_poliza', 'estado_poliza'),
             ('fecha_expedicion', 'fecha_inicio', 'fecha_fin',),
             ('es_renovable',),
         )
         },
    ]


class Tramites(Datatables):
    modal_width = 900
    model = Tramite
    list_display = ('code', 'aseguradora', 'tipo_tramite', 'cliente', 'descripcion', 'estado')
    search_fields = ('code', 'descripcion')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('code', 'aseguradora', 'tipo_tramite'),
                ('cliente', 'estado'),
                ('descripcion',),
            )
        },
    ]


class Endosos(Datatables):
    modal_width = 900
    model = Endoso
    list_display = ('cliente', 'tipo_endoso', 'fecha_emision', 'fecha_fin', 'fecha_recepcion',
                    'comision', 'prima_neta', 'derecho_emision', 'bomberos', 'recargo_descuento', 'iva',
                    'otros', 'prima_total', 'forma_pago', 'cuotas', 'observaciones', 'estado')

    search_fields = ('cliente', 'observaciones')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('cliente', 'tipo_endoso'),
                ('forma_pago', 'cuotas', 'estado'),
                ('fecha_emision', 'fecha_fin', 'fecha_recepcion'),
                ('comision', 'prima_neta', 'derecho_emision', 'bomberos'),
                ('recargo_descuento', 'iva', 'otros', 'prima_total'),
                ('observaciones',),
            )
        },
    ]

# endregion
