from django.shortcuts import render
from .generics import Datatables
from django.contrib.auth.decorators import login_required
from cotizador.forms import *
from .forms import *
from .widgets import TableBordered, TableBorderedInput


# @staff_member_required
# def documentos(request):
#     if request.method == "GET":
#         files = []
#         try:
#             type = ContentType.objects.get(app_label=request.GET.get('app_label'),
#                                            model=request.GET.get('model'))
#             original = type.get_object_for_this_type(id=int(request.GET.get('id')))
#         except:
#             original = None
#             type = None
#         if original:
#             files = Archivo.objects.filter(type=type, key=original.id)
#         return render(request, 'trustseguros/documentos_adjuntos.html',
#                       {'archivos': files, 'catalogos': catalogoArchivo.objects.all().order_by('nombre'),
#                        'original': original.to_json()})
#
#     if request.method == "POST":
#         if 'new' in request.POST:
#             file = None
#             try:
#                 type = ContentType.objects.get(app_label=request.POST.get('app_label'),
#                                                model=request.POST.get('model'))
#                 original = type.get_object_for_this_type(id=int(request.POST.get('id')))
#             except:
#                 type = None
#                 original = None
#             if original:
#                 file = Archivo()
#                 document = request.FILES['file']
#                 file.nombre = document.name
#                 file.catalogo = request.POST.get('catalogo')
#                 file.fecha_caducidad = request.POST.get('fecha_caducidad')
#                 file.archivo = document
#                 file.type = type
#                 file.key = original.id
#                 file.save()
#                 print(file)
#             return render(request, 'trustseguros/include/row_document.html', {
#                 'archivo': file.to_json(), 'catalogos': catalogoArchivo.objects.all().order_by('nombre')
#             })
#         if 'update' in request.POST:
#             print(request.POST)
#             a = Archivo.objects.get(id=int(request.POST.get('id')))
#             a.nombre = request.POST.get('nombre')
#
#             try:
#                 a.catalogo = catalogoArchivo.objects.get(id=int(request.POST.get('catalogo')))
#             except:
#                 pass
#
#             try:
#                 a.fecha_caducidad = request.POST.get('fecha')
#             except:
#                 pass
#
#             a.save()
#             return JsonResponse(a.to_json(), encoder=Codec)
#         if 'delete' in request.POST:
#             Archivo.objects.get(id=int(request.POST.get('id'))).delete()
#             return JsonResponse({})
#
#
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
    return render(request, 'trustseguros/lte/index.html', {

    })


class Prospectos(Datatables):
    modal_width = 1200
    model = ClienteProspecto
    form = ProspectoForm
    form_template = "trustseguros/lte/prospecto-form.html"
    list_display = ('nombre', 'telefono')
    list_filter = ('tipo_cliente', )
    search_fields = ('razon_social', 'ruc', 'cedula', 'primer_nombre', 'segundo_nombre',
                     'apellido_materno', 'apellido_materno')
    media = {
        'js': ['trustseguros/lte/js/municipio.js', 'trustseguros/lte/js/tipo.cliente.js']
    }


class PersonaNatural(Datatables):
    modal_width = 1200
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
                ('cedula', 'email_personal'),
                ('telefono', 'celular'),
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
                ('user', 'cambiar_pass',),
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
            'id': 'polizas',
            'name': 'Pólizas',
            'fields': (
                ('polizas',),
            )
        },
        {
            'id': 'tramites',
            'name': 'Trámites',
            'fields': (
                ('tramites',),
            )
        },
        # {
        #     'id': 'sepelio',
        #     'name': 'Dependientes seguro de sepelio',
        #     'fields': (
        #         ('dependientes_sepelio',),
        #     )
        # },
        # {
        #     'id': 'accidentes',
        #     'name': 'Dependientes seguro de accidentes',
        #     'fields': (
        #         ('dependientes_accidente',),
        #     )
        # },
    ]
    media = {
        'js': ['trustseguros/lte/js/municipio.js', ]
    }


class PersonaJuridica(Datatables):
    modal_width = 1200
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
                ('departamento', 'municipio'),
                ('domicilio',),
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
            'id': 'polizas',
            'name': 'Pólizas',
            'fields': (
                ('polizas',),
            )
        },
        {
            'id': 'tramites',
            'name': 'Trámites',
            'fields': (
                ('tramites',),
            )
        },
    ]
    media = {
        'js': ['trustseguros/lte/js/municipio.js', ]
    }

    def save_related(self, instance, data):
        for i in range(1, len(data.getlist('contacto_id'))):
            if data.getlist('contacto_id')[i] == '':
                c = Contacto(contacto=instance)
            else:
                c = Contacto.objects.get(id=int(data.getlist('contacto_id')[i]))
            c.nombre = data.getlist('cliente_contacto-nombre')[i]
            c.cedula = data.getlist('cliente_contacto-cedula')[i]
            c.telefono = data.getlist('cliente_contacto-telefono')[i]
            c.celular = data.getlist('cliente_contacto-celular')[i]
            c.email_personal = data.getlist('cliente_contacto-email_personal')[i]
            c.save()


class Aseguradoras(Datatables):
    model = Aseguradora
    list_display = ('name', 'phone', 'address', 'emision', )
    fieldsets = [
        {
            'id': 'info',
            'name': 'Información general',
            'fields': (
                ('name', 'ruc'),
                ('phone', 'email'),
                ('emision', ),
                ('address',),
            )
        },
    ]


class Tickets(Datatables):
    modal_width = 1200
    model = Ticket
    form = LteTicketForm
    list_display = ('code', 'nombres', 'apellidos', 'cedula')

    search_fields = ('code',)
    fieldsets = [
        {
            'id': 'info',
            'name': 'Datos del cliente',
            'fields': (
                ('code', 'cliente'),
                ('nombres', 'apellidos'),
                ('email', 'cedula'),
                ('celular', 'telefono'),
                ('domicilio',),
            )
        },
        # {
        #     'id': 'sepelio',
        #     'name': 'Dependientes seguro de sepelio',
        #     'fields': (
        #         ('dependientes_sepelio',),
        #     )
        # },
        # {
        #     'id': 'accidentes',
        #     'name': 'Dependientes seguro de accidentes',
        #     'fields': (
        #         ('dependientes_accidente',),
        #     )
        # },
    ]

    #
    # def save_related(self, instance, data):
    #     print(data)
    #     profile = instance.profile()
    #     profile.primer_nombre = data['primer_nombre']
    #     profile.segundo_nombre = data['segundo_nombre']
    #     profile.apellido_paterno = data['apellido_paterno']
    #     profile.apellido_materno = data['apellido_materno']
    #     profile.email_personal = data['email_personal']
    #     profile.cedula = data['cedula']
    #     profile.celular = data['celular']
    #     profile.telefono = data['telefono']
    #     profile.departamento_id = data['departamento']
    #     profile.municipio_id = data['municipio']
    #     profile.domicilio = data['domicilio']
    #     profile.sucursal = data['sucursal']
    #     profile.codigo_empleado = data['codigo_empleado']
    #     profile.cargo = data['cargo']
    #     #profile.cambiar_pass = data['cambiar_pass']
    #     profile.save()
    #
    # form_template = "trustseguros/lte/perfilusuario-form.html"
    # list_template = "trustseguros/lte/perfilusuario-table.html"


class DependientesSepelio(Datatables):
    model = benSepelio
    form = LteSepelioForm
    list_display = ('parentesco', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    search_fields = ('primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    list_filter = ('empleado',)
    fieldsets = [
        {
            'id': 'info',
            'name': 'Datos del dependiente',
            'fields': (
                ('parentesco', 'empleado'),
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('fecha_nacimiento', 'suma_asegurada', 'numero_poliza'),
            )
        },
    ]


class DependientesAccidente(Datatables):
    model = benAccidente
    form = LteAccidentetForm
    list_display = ('parentesco', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    search_fields = ('parentesco', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    fieldsets = [
        {
            'id': 'info',
            'name': 'Datos del dependiente',
            'fields': (
                ('parentesco', 'empleado'),
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('fecha_nacimiento', 'suma_asegurada', 'numero_poliza'),
            )
        },
    ]


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
        {
            'id': 'campos-adicionales',
            'name': 'Campos adicionales',
            'fields': (
                ('campos_adicionales',),
            )
        },
    ]

    def save_related(self, instance, data):
        for i in range(1, len(data.getlist('campoadicional_id'))):
            if data.getlist('campoadicional_id')[i] == '':
                c = CampoAdicional(ramo=instance)
            else:
                c = CampoAdicional.objects.get(id=int(data.getlist('campoadicional_id')[i]))
            f = CampoAdicionalForm({
                'ramo_campo_adicional-name': data.getlist('ramo_campo_adicional-name')[i],
                'ramo_campo_adicional-label': data.getlist('ramo_campo_adicional-label')[i],
            }, instance=c)
            if f.is_valid():
                f.save()


class Grupos(Datatables):
    model = Grupo
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)


class SubRamos(Datatables):
    modal_width = 1200
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
            )
        },
        {
            'id': 'coberturas',
            'name': 'Coberturas que aplica',
            'fields': (
                ('coberturas', ),
            )
        }
    ]

    def save_related(self, instance, data):
        for i in range(1, len(data.getlist('cobertura_id'))):
            if data.getlist('cobertura_id')[i] == '':
                c = Cobertura(sub_ramo=instance)
            else:
                c = Cobertura.objects.get(id=int(data.getlist('cobertura_id')[i]))
            f = CoberturaForm({
                'subramo_cobertura-name': data.getlist('subramo_cobertura-name')[i],
                'subramo_cobertura-tipo_calculo': data.getlist('subramo_cobertura-tipo_calculo')[i],
                'subramo_cobertura-tipo_cobertura': data.getlist('subramo_cobertura-tipo_cobertura')[i],
                'subramo_cobertura-tipo_exceso': data.getlist('subramo_cobertura-tipo_exceso')[i],
                # 'subramo_cobertura-iva': data.getlist('subramo_cobertura-iva')[i],
            }, instance=c)
            if f.is_valid():
                f.save()


class PolizasAutomovil(Datatables):
    modal_width = 1600
    model = Poliza
    form = PolizaForm
    list_template = 'trustseguros/lte/poliza-datatables.html'
    form_template = 'trustseguros/lte/poliza-modal.html'
    list_display = ('no_poliza', 'no_recibo', 'cliente.nombre', 'fecha_emision', 'fecha_vence')
    search_fields = ('no_poliza', 'no_recibo', 'nombres', 'apellidos')
    list_filter = ('grupo', 'ramo')

    def save_related(self, instance, data):
        print('instance', instance)
        print('data', data)



# endregion
