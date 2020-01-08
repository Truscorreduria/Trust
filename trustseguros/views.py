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
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.query_utils import DeferredAttribute
from django.contrib.auth.decorators import login_required


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

@login_required(login_url="/cotizador/login/")
def index(request):
    return render(request, 'trustseguros/lte/index.html', {

    })


class Filter:
    def __init__(self, field_name, model, option="=",
                 template_name="trustseguros/lte/filters/select-filter.html"):
        self.model = model
        self.field_name = field_name
        self.option = option
        self.template_name = template_name
        self.field = self.get_field()

    def get_form(self):
        return modelform_factory(self.model, fields=(self.field_name,))

    def get_field(self):
        field = getattr(self.model, self.field_name, None)
        if not field:
            raise ValueError('field not exist')
        return field

    def get_model_choices(self):
        return [{'value': x.id, 'name': str(x)} for x in self.field.get_queryset()]

    def get_value(self, instance):
        return getattr(instance, self.field_name)

    def get_value_display(self, instance):
        try:
            return getattr(instance, 'get_%s_display' % self.field_name)
        except:
            return getattr(instance, self.field_name)

    def get_distinct_choices(self):
        return [{'value': self.get_value(x), 'name': self.get_value_display(x)}
                for x in self.model.objects.all().distinct(self.field_name).order_by(self.field_name)]

    def get_bool_choices(self):
        return [{'value': '1', 'name': 'Si'}, {'value': '0', 'name': 'No'}, ]

    def render(self):
        print(type(self.field))
        if isinstance(self.field, ForwardManyToOneDescriptor):
            return render_to_string(self.template_name, context={
                'field_name': self.field_name,
                'option': self.option,
                'choices': self.get_model_choices(),
                'table_field': '%s_id' % self.field_name,
                'form': self.get_form(),
            })
        if isinstance(self.field, DeferredAttribute):
            return render_to_string(self.template_name, context={
                'field_name': self.field_name,
                'option': '__icontains=',
                'table_field': self.field_name,
                'choices': self.get_distinct_choices(),
                'form': self.get_form(),
            })
        if isinstance(self.field, bool):
            return render_to_string(self.template_name, context={
                'field_name': self.field_name,
                'option': self.option,
                'table_field': self.field_name,
                'choices': self.get_bool_choices(),
                'form': self.get_form(),
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
    list_filter = ()

    @classmethod
    def as_view(cls, **initkwars):
        return login_required(super().as_view(**initkwars), login_url="/cotizador/login/")

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

    def html_form(self, instance, request, form, method):
        return render_to_string(self.form_template,
                                context={'opts': self.model._meta, 'fieldsets': self.fieldsets,
                                         'form': form, 'instance': instance, 'method': method},
                                request=request)

    def get_list_filters(self):
        return [Filter(x, self.model) for x in self.list_filter]

    def get(self, request):
        return render(request, self.list_template, {
            'opts': self.model._meta, 'list_display': self.list_display,
            'form': self.get_form(), 'form_template': self.form_template,
            'modal_width': self.modal_width, 'media': self.media,
            'list_filter': self.get_list_filters()

        })

    def save_related(self, instance, data):
        pass

    def get_filters(self, filters):
        return [Q((field.split('=')[0], field.split('=')[1])) for field in filters.split('&')]

    def search_value(self, search_value):
        return [
            Q(('{}__icontains'.format(field), word))
            for word in search_value.split(' ')
            for field in self.search_fields
        ]

    def get_queryset(self, filters, search_value):
        queryset = self.model.objects.all()
        print(filters)
        if not filters == "":
            queryset = queryset.filter(reduce(operator.and_, self.get_filters(filters)))
        if search_value:
            queryset = queryset.filter(reduce(operator.or_, self.search_value(search_value)))
        return queryset

    def get_ordered_queryset(self, filters, search_value, order):
        queryset = self.get_queryset(filters, search_value)
        return queryset.order_by(order)

    def get_data(self, start, per_page, filters, search_value, draw, order=None):
        queryset = self.get_queryset(filters, search_value)
        if order:
            queryset = self.get_ordered_queryset(filters, search_value, order)
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
        status = 200
        errors = []
        instance = None

        if 'list' in request.POST:
            order = None
            start = int(request.POST.get('start', 0))
            draw = int(request.POST.get('draw', 0))
            per_page = int(request.POST.get('length', 10))
            search_value = request.POST.get('search[value]', None)
            filters = request.POST.get('filters', None)
            order_column = request.POST.get('order[0][column]', None)
            order_dir = request.POST.get('order[0][dir]', None)

            if order_column and order_dir:
                order = ''
                if order_dir == 'desc':
                    order += '-'
                order += self.list_display[int(order_column)].split('.')[0]

            return JsonResponse(self.get_data(start, per_page, filters, search_value, draw, order), encoder=Codec)
        if 'open' in request.POST:
            instance = self.model.objects.get(id=int(request.POST.get('id')))
            form = self.get_form()(instance=instance)
            html_form = self.html_form(instance, request, form, 'POST')
        if 'save' in request.POST:
            instance = self.model.objects.get(id=int(request.POST.get('id')))
            form = self.get_form()(request.POST, instance=instance)
            html_form = self.html_form(instance, request, form, 'POST')
            if form.is_valid():
                form.save()
                instance = form.instance
                self.save_related(instance=instance, data=form.cleaned_data)
            else:
                errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                status = 203
                print(errors)

        return JsonResponse({'instance': instance.to_json(),
                             'form': html_form, 'errors': errors}, encoder=Codec,
                            status=status)

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
                    status = 200
                    self.save_related(instance=instance, data=request.PUT)
                else:
                    errors = [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]
                    html_form = self.html_form(instance, request, form, "PUT")
            except IntegrityError as e:
                print(e)
                # errors.append(dict(e))

        return JsonResponse({'instance': instance.to_json(), 'form': html_form,
                             'errors': errors}, status=status, encoder=Codec)


class Aseguradoras(Datatables):
    modal_width = 900
    model = Aseguradora
    list_display = ('nombre', 'ruc', 'email', 'telefono', 'direccion')
    search_fields = ('nombre', 'ruc', 'email', 'telefono')
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
    list_filter = ('departamento', 'nombre')
    media = {
        'js': ['trustseguros/lte/js/municipio.js', 'trustseguros/lte/js/filter-municipio.js', ]
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
        'js': ['trustseguros/lte/js/municipio.js', ]
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
        'js': ['trustseguros/lte/js/municipio.js', ]
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

    list_filter = ('tipo',)


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


from cotizador.models import PerfilEmpleado, Poliza as PolizaAutomovil, Ticket as TicketCotizador, \
    benSepelio, benAccidente
from django.forms.models import model_to_dict
from .widgets import TableBordered, TableBorderedInput


def user_to_json(user):
    o = dict(id=user.id, username=user.username, email=user.email,
             first_name=user.first_name, last_name=user.last_name)
    o['app_label'] = user._meta.app_label
    o['model'] = user._meta.object_name.lower()
    return o


User.add_to_class('to_json', user_to_json)


class UsuarioCotizadorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(id__in=PerfilEmpleado.objects.all().values_list('user', flat=True))

    def normalize_email(self, email):
        return email


class UsuarioCotizador(User):
    objects = UsuarioCotizadorManager()
    class Meta:
        proxy = True

    def to_json(self):
        o = super().to_json()
        o['perfil'] = try_json(self.profile(), PerfilEmpleado)
        return o


class UsuarioCotizadorForm(forms.ModelForm):
    password = forms.CharField(max_length=255, required=False)
    primer_nombre = forms.CharField(max_length=125, required=False)
    segundo_nombre = forms.CharField(max_length=125, required=False)
    apellido_paterno = forms.CharField(max_length=125, required=False)
    apellido_materno = forms.CharField(max_length=125, required=False)
    email_personal = forms.EmailField(max_length=255, required=False)
    cedula = forms.CharField(max_length=14, required=False)
    celular = forms.CharField(max_length=8, required=False)
    telefono = forms.CharField(max_length=8, required=False)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    municipio = forms.ModelChoiceField(queryset=Municipio.objects.all(), required=False)
    domicilio = forms.CharField(max_length=250, required=False)
    sucursal = forms.CharField(max_length=60, required=False)
    codigo_empleado = forms.CharField(max_length=14, required=False)
    cargo = forms.CharField(max_length=60, required=False)
    cambiar_pass = forms.BooleanField(initial=False, required=False, label="cambio de password",
                                      help_text="obligar al usuario a cambiar en password en el siguiente inicio de sesión")

    dependientes_sepelio = forms.Field(required=False, label="", widget=TableBordered(
        attrs={
            'columns': (('parentesco', 'Parentezco'), ('primer_nombre', 'Primer nombre'),
                        ('segundo_nombre', 'Segundo nombre'), ('apellido_paterno', 'Apellido materno'),
                        ('apellido_materno', 'Apellido materno'), ('costo', 'Costo'),
                        ('suma_asegurada', 'Suma asegurada')
                        )
        }
    ))

    dependientes_accidente = forms.Field(required=False, label="", widget=TableBordered(
        attrs={
            'columns': (('parentesco', 'Parentezco'), ('primer_nombre', 'Primer nombre'),
                        ('segundo_nombre', 'Segundo nombre'), ('apellido_paterno', 'Apellido materno'),
                        ('apellido_materno', 'Apellido materno'), ('costo', 'Costo'),
                        ('suma_asegurada', 'Suma asegurada')
                        )
        }
    ))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            profile = instance.profile()
            kwargs.update(initial={
                'primer_nombre': profile.primer_nombre,
                'segundo_nombre': profile.segundo_nombre,
                'apellido_paterno': profile.apellido_paterno,
                'apellido_materno': profile.apellido_materno,
                'email_personal': profile.email_personal,
                'cedula': profile.cedula,
                'celular': profile.celular,
                'telefono': profile.telefono,
                'departamento': profile.departamento,
                'municipio': profile.municipio,
                'domicilio': profile.domicilio,
                'sucursal': profile.sucursal,
                'codigo_empleado': profile.codigo_empleado,
                'cargo': profile.cargo,
                'dependientes_sepelio': profile.dependientes_sepelio(),
                'dependientes_accidente': profile.dependientes_accidente(),
            })
        super().__init__(*args, **kwargs)


class Usuarios(Datatables):
    modal_width = 1200
    model = UsuarioCotizador
    list_display = ('username', 'email',
                    ('Primer Nombre', 'perfil.primer_nombre'),
                    ('Segundo Nombre', 'perfil.segundo_nombre'),
                    ('Primer Apellido', 'perfil.apellido_paterno'),
                    ('Segundo Apellido', 'perfil.apellido_materno'),
                    )
    list_filter = ('is_active',)
    search_fields = ('username', 'email')
    form = UsuarioCotizadorForm
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información General',
            'fields': (
                ('username', 'email'),
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('cedula', 'email_personal'),
                ('telefono', 'celular'),
                ('departamento', 'municipio'),
                ('domicilio',),
                ('sucursal', 'codigo_empleado', 'cargo'),
                ('date_joined', 'last_login'),
                ('cambiar_pass', 'is_active'),
            )
        },
        {
            'id': 'sepelio',
            'name': 'Dependientes seguro de sepelio',
            'fields': (
                ('dependientes_sepelio',),
            )
        },
        {
            'id': 'accidentes',
            'name': 'Dependientes seguro de accidentes',
            'fields': (
                ('dependientes_accidente',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/lte/js/municipio.js', 'trustseguros/lte/js/cambiar-pass.js', ]
    }

    def save_related(self, instance, data):
        print(data)
        profile = instance.profile()
        profile.primer_nombre = data['primer_nombre']
        profile.segundo_nombre = data['segundo_nombre']
        profile.apellido_paterno = data['apellido_paterno']
        profile.apellido_materno = data['apellido_materno']
        profile.email_personal = data['email_personal']
        profile.cedula = data['cedula']
        profile.celular = data['celular']
        profile.telefono = data['telefono']
        profile.departamento_id = data['departamento']
        profile.municipio_id = data['municipio']
        profile.domicilio = data['domicilio']
        profile.sucursal = data['sucursal']
        profile.codigo_empleado = data['codigo_empleado']
        profile.cargo = data['cargo']
        #profile.cambiar_pass = data['cambiar_pass']
        profile.save()

    form_template = "trustseguros/lte/perfilusuario-form.html"
    list_template = "trustseguros/lte/perfilusuario-table.html"


class DependientesSepelio(Datatables):
    model = benSepelio
    list_display = ('parentesco', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    search_fields = ('primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    list_filter = ('empleado', )
    fieldsets = [
        {
            'id': 'info',
            'name': 'Datos del dependiente',
            'fields': (
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('parentesco',),
                ('fecha_nacimiento', 'suma_asegurada', 'numero_poliza'),
            )
        },
    ]


class DependientesAccidente(Datatables):
    model = benAccidente
    list_display = ('parentesco', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    search_fields = ('parentesco', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Datos del dependiente',
            'fields': (
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('empleado', 'parentesco'),
                ('fecha_nacimiento', 'suma_asegurada', 'numero_poliza'),
            )
        },
    ]


class PolizasAutomovil(Datatables):
    modal_width = 1000
    model = PolizaAutomovil
    list_display = ('fecha_emision', 'no_poliza', 'no_recibo', 'nombres', 'apellidos')
    fieldsets = [
        {
            'id': 'info',
            'name': "Datos de la póliza",
            'fields': (
                ('fecha_emision', 'fecha_vence', 'no_poliza', 'aseguradora'),
                ('nombres', 'apellidos'),
                ('cedula', 'telefono', 'celular'),
                ('domicilio',)
            )
        },
        {
            'id': 'cobertura',
            'name': "Detalles de coberturas",
            'fields': (
                ('fecha_pago', 'no_recibo', 'tipo_cobertura'),
                ('marca', 'modelo', 'anno', 'color'),
                ('chasis', 'motor', 'circulacion', 'placa'),

                ('minimo_deducible', 'porcentaje_deducible', 'deducible_rotura_vidrios'),
                ('porcentaje_deducible_extension', 'minimo_deducible_extension'),
            )
        },
        {
            'id': 'pago',
            'name': "Método y forma de pago",
            'fields': (
                ('costo_exceso', 'monto_exceso', 'valor_nuevo', 'suma_asegurada'),
                ('subtotal', 'emision', 'iva', 'total'),
                ('forma_pago', 'cuotas', 'monto_cuota'),
                ('medio_pago', 'cesion_derecho', 'beneficiario'),
            )
        },
    ]

# endregion
