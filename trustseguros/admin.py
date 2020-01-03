from django.contrib import admin
from .models import *
from .forms import EndosoForm, ClienteForm, PolizaForm, GrupoForm, BeneficiarioForm, TramiteForm
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin


class MediaAdminMixin:
    change_form_template = "trustseguros/media_mixin.html"


class subramoTabular(admin.TabularInline):
    model = SubRamo
    extra = 0
    classes = ('grp-collapse', 'grp-open')
    fields = ('nombre', 'ramo')


@admin.register(Ramo)
class ramoAdmin(admin.ModelAdmin):
    inlines = [subramoTabular, ]


class contactoTabular(admin.TabularInline):
    model = Contacto
    extra = 0
    classes = ('grp-collapse', 'collapse-open')
    fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
              'telefono', 'puesto', 'email_principal')

    class Media:
        css = {
            'all': ('trustseguros/css/contacto.css',)
        }


@admin.register(Aseguradora)
class aseguradoraAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'ruc', 'email')
    inlines = [contactoTabular, ]
    fieldsets = (
        ('Información General', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('nombre', 'ruc'),
                ('telefono', 'email'),
                ('cuenta_bancaria'),
                ('departamento', 'municipio'),
                ('direccion'),
            ),
        }),
    )

    class Media:
        js = ('cotizador/js/municipio.js',)


@admin.register(Cliente)
class clienteAdmin(MediaAdminMixin, admin.ModelAdmin):
    inlines = [contactoTabular, ]
    list_display = ('full_name', 'numero_identificacion', 'telefono', 'celular', 'email_principal',
                    'email_alterno')

    search_fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido',
                     'segundo_apellido', 'razon_social', 'telefono', 'celular', 'email_principal',
                     'email_alterno')

    list_filter = ('tipo',)
    form = ClienteForm
    change_list_template = "trustseguros/clientes.html"
    fieldsets = (

        (None, {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('tipo',)
        }),

        ('Información Persona Natural', {
            'classes': ('grp-collapse', 'grp-open', 'fields-persona-natural'),
            'fields': (('primer_nombre', 'segundo_nombre'),
                       ('primer_apellido', 'segundo_apellido'),
                       ('genero', 'estado_civil'),
                       ('tipo_identificacion', 'numero_identificacion'),
                       ('fecha_nacimiento',),
                       'ocupacion')
        }),

        ('Información Persona Jurídica', {
            'classes': ('grp-collapse', 'grp-open', 'fields-persona-juridica'),
            'fields': (
                ('razon_social', 'ruc'),
                ('actividad_economica'),
                ('pagina_web'),
                ('fecha_constitucion', 'fecha_expedicion'),
                ('observaciones'),
            ),
        }),

        ('Información General', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (('telefono', 'celular'),
                       ('departamento', 'municipio'),
                       'direccion',
                       ('email_principal', 'email_alterno'),)
        }),

        ('Otras Opciones', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('sms_cartera_vencer', 'sms_poliza_vencer'),
                ('correo_cartera_vencer', 'correo_poliza_vencer'),
                ('link_accesso', 'usuario'),
            ),
        }),

        ('Lista de polizas', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('lista_polizas',),
        }),
    )

    class Media:
        js = ('cotizador/js/municipio.js', 'trustseguros/js/tipo.cliente.js')


@admin.register(Tramite)
class tramiteAdmin(SimpleHistoryAdmin):
    form = TramiteForm
    change_form_template = "trustseguros/tramite.html"
    history_list_display = ["estado"]
    list_display = ('code', 'cliente', 'aseguradora', 'poliza', 'estado')
    search_fields = ('code',)
    list_filter = ('estado',)
    fieldsets = (
        ('Datos del Trámite', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('code', 'tipo_tramite'),
                ('cliente',),
                ('aseguradora', 'poliza'), 'descripcion',
                ('estado'),
            )
        }),
    )
    readonly_fields = ('code',)


@admin.register(Grupo)
class grupoAdmin(MediaAdminMixin, admin.ModelAdmin):
    date_hierarchy = 'fecha_expedicion'
    list_display = ('nombre_grupo', 'aseguradora', 'cliente', 'fecha_inicio', 'fecha_fin')
    form = GrupoForm
    fieldsets = (
        ('Datos del Grupo', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('nombre_grupo', 'aseguradora'), 'cliente',
                ('fecha_inicio', 'fecha_fin'))
        }),
        ('Polizas del grupo', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('polizas_grupo',)
        }),
    )


class beneficiarioTabular(admin.TabularInline):
    model = Beneficiario
    form = BeneficiarioForm
    fields = ('cliente',)
    extra = 0
    classes = ('grp-collapse', 'grp-open')


@admin.register(Poliza)
class polizaAdmin(MediaAdminMixin, ImportExportModelAdmin):
    date_hierarchy = 'fecha_expedicion'
    change_form_template = "trustseguros/poliza.html"
    form = PolizaForm
    list_filter = ('tipo', 'sub_ramo')
    fieldsets = (
        ('Datos Principales', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('aseguradora', 'tipo'),
                ('grupo', 'sub_ramo', 'vendedor'),
                ('cliente',),
                ('numero_poliza', 'estado_poliza'),
                ('fecha_expedicion', 'fecha_inicio', 'fecha_fin'),
                ('es_renovable', 'beneficiaro_oneroso')
            ),
        }),
        ('Observaciones', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('observaciones_internas', 'observaciones_cliente'),
        }),
        ('Detalle de Costos', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('prima_neta', 'derecho_emision'),
                ('recargo_descuento', 'iva'),
                ('otros', 'prima_total'),
                ('porcentaje_comision', 'monto_comision'),
                ('comision_agencia', 'monto_agencia'),
            ),
        }),
        ('Otras Opciones', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('correo_poliza_vencer', 'correo_cartera_vencer'),
                ('sms_poliza_vencer', 'sms_cartera_vencer'),
            ),
        }),
        ('Lista de endosos', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('lista_endosos',),
        }),
    )
    inlines = [beneficiarioTabular, ]
    change_list_template = 'trustseguros/admin/poliza.html'
    list_display = ('numero_poliza', 'cliente', 'tipo', 'sub_ramo',
                    'prima_neta', 'derecho_emision', 'recargo_descuento', 'iva', 'otros', 'prima_total',
                    'monto_comision')
    search_fields = ('numero_poliza', 'cliente__primer_nombre', 'cliente__primer_apellido',
                     'cliente__numero_identificacion')

    class Media:
        css = {
            'all': ('trustseguros/css/poliza.css',)
        }


@admin.register(Endoso)
class endosoAdmin(MediaAdminMixin, admin.ModelAdmin):
    '''
    Compañia, Nombre del cliente, Numero de poliza
    '''
    date_hierarchy = 'fecha_emision'
    list_display = ('recibo_prima', 'tipo_endoso', 'estado', 'user', 'aseguradora',
                    'contratante', 'poliza')
    list_filter = ('tipo_endoso',)
    form = EndosoForm
    change_form_template = "trustseguros/endoso.html"
    fieldsets = (
        ('Datos Principales', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('tipo_endoso', 'recibo_prima'),
                ('cliente',),
                ('tramite', 'poliza'),
                ('descripcion'), ('observaciones',),
                ('fecha_emision', 'fecha_recepcion', 'fecha_fin'),
                ('prima_neta', 'derecho_emision', 'comision'),
                ('bomberos', 'recargo_descuento'),
                ('iva', 'otros'),
                ('prima_total', 'estado'),
            ),
        }),
        ('Forma de pago', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': ('forma_pago', 'cuotas'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('trustseguros/js/comision.js',)


@admin.register(Vendedor)
class vendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje_comision', 'porcentaje_sub_comision', 'porcentaje_retencion',
                    'total_comision')
    fieldsets = (
        ('Datos Principales', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('nombre'),
                ('email', 'telefono'),
                ('porcentaje_comision', 'porcentaje_sub_comision'),
                ('porcentaje_retencion', 'total_comision'),
            ),
        }),
    )


@admin.register(catalogoArchivo)
class catalogoAdmin(admin.ModelAdmin):
    pass


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    change_list_template = "trustseguros/admin/certificado.html"
    list_display = ('numero', 'tipo', 'poliza')
    list_filter = ('tipo', )

    def get_fields(self, request, obj=None):
        if obj and obj.tipo == 'persona':
            return ('numero', 'tipo', 'poliza', 'suma_asegurada', 'primer_nombre', 'segundo_nombre', 'primer_apellido',
                    'segundo_apellido', 'tipo_persona', 'parentesco', 'cedula', 'fecha_nacimiento',)
        if obj and obj.tipo == 'auto':
            return (
            'numero', 'tipo', 'poliza', 'suma_asegurada', 'marca', 'modelo', 'placa', 'anno', 'motor', 'chasis',)
        if obj and obj.tipo == 'edificio':
            return ('numero', 'tipo', 'poliza', 'suma_asegurada', 'ubicacion', )
