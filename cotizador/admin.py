from django.contrib import admin
from image_cropping.admin import ImageCroppingMixin
from grappelli_extras.admin import entidad_admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .views import reporte_inclusion
from .forms import MarcaRecargoForm


@admin.register(Aseguradora)
class AseguradoraAdmin(ImageCroppingMixin, entidad_admin):
    fields = (('name', 'active'), ('emision', 'phone'), 'address', 'logo', 'cropping')
    list_display = ('name', 'phone', 'address', 'active')


class AntiguedadList(admin.TabularInline):
    model = Anno
    extra = 0
    classes = ('grp-collapse', 'grp-open')


@admin.register(Depreciacion)
class DepreciacionAdmin(admin.ModelAdmin):
    list_display = ('aseguradora',)
    inlines = [AntiguedadList, ]
    save_as = True


class ModeloListFilter(admin.SimpleListFilter):
    """
    This filter is an example of how to combine two different Filters to work together.
    """
    # Human-readable title which will be displayed in the right admin sidebar just above the filter
    # options.
    title = 'modelo'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'modelo'

    # Custom attributes
    related_filter_parameter = 'marca'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_questions = []
        queryset = Referencia.objects.order_by('marca')
        if self.related_filter_parameter in request.GET:
            queryset = queryset.filter(marca=request.GET[self.related_filter_parameter])
        for referencia in queryset:
            list_of_questions.append(
                (str(referencia.modelo), referencia.modelo)
            )
        return sorted(list_of_questions, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(modelo=self.value())
        return queryset


@admin.register(Referencia)
class ReferenciaAdmin(ImportExportModelAdmin):
    list_display = ('marca', 'modelo', 'anno', 'valor', 'chasis', 'motor')
    search_fields = ('marca', 'modelo', 'chasis')
    list_filter = ('marca', ModeloListFilter, 'anno')


@admin.register(Poliza)
class PolizaAdmin(ImportExportModelAdmin):
    date_hierarchy = 'fecha_emision'
    list_display = (
    'print_code', 'fecha_emision', 'no_poliza', 'marca', 'modelo', 'anno', 'user', 'chasis', 'valor_nuevo',
    'suma_asegurada', 'subtotal', 'emision', 'iva', 'total', 'medio_pago', 'fecha_vence')
    search_fields = ('code', 'nombres', 'apellidos', 'marca', 'modelo', 'chasis', 'no_poliza')
    list_filter = ('marca', 'tipo_cobertura', 'medio_pago')
    change_form_template = 'cotizador/admin/poliza.html'

    fieldsets = (
        ('Datos Personales', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('fecha_emision', 'user'),
                ('nombres', 'apellidos'),
                ('cedula', 'tipo_cobertura'),
                ('telefono', 'celular'),
                ('cesion_derecho', 'beneficiario'),
                'domicilio'
            )
        }),
        ('Datos del Vehículo', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('marca', 'modelo', 'anno'),
                ('chasis', 'motor', 'placa'),
                ('color'),
            )
        }),
        ('Datos de Pago', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                ('forma_pago', 'medio_pago'),
                ('cuotas', 'monto_cuota'),
                'valor_nuevo', 'suma_asegurada',
                'subtotal', 'emision',
                ('iva', 'monto_exceso'),
                ('total', 'costo_exceso')
            )
        }),
        ('Documentos', {
            'classes': ('grp-collapse', 'grp-closed'),
            'fields': (
                'file_circulacion', 'file_cedula', 'file_carta'
            )
        }),
    )

    readonly_fields = ('no_poliza', 'no_recibo')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('code', 'created', 'referente', 'movimiento', 'poliza', 'descripcion',
                    'nombres', 'apellidos', 'cedula', 'email', 'telefono', 'estado')
    list_filter = ('referente', 'movimiento', 'estado')
    search_fields = ('nombres', 'apellidos', 'cedula', 'email', 'telefono')
    # fieldsets = (
    #     ('', {
    #         'classes': ('grp-collapse', 'grp-open'),
    #         'fields': ('code', 'descripcion')
    #     }),
    #     ('Datos suministrados por el cliente', {
    #         'classes': ('grp-collapse', 'grp-open'),
    #         'fields': (('marca', 'anno', 'modelo'), ('chasis', 'motor'),
    #                    ('placa', 'color'), ('uso', 'circulacion'))
    #     }),
    #     ('', {
    #         'classes': ('grp-collapse', 'grp-open'),
    #         'fields': ('valor_nuevo', 'suma_asegurada', 'subtotal', 'emision', 'iva', 'total')
    #     }),
    # )

    change_form_template = 'cotizador/admin/ticket.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {'aseguradora': Aseguradora.objects.get(name="ASSA")}
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    # readonly_fields = ('code', 'marca', 'anno', 'modelo', 'placa', 'color', 'uso', 'circulacion',
    #                   'chasis', 'motor')


admin.site.register(Entidad, entidad_admin)


class beneficiarios_sepelio(admin.TabularInline):
    model = benSepelio
    extra = 0
    classes = ('grp-collapse', 'grp-open')


class beneficiarios_accidente(admin.TabularInline):
    model = benAccidente
    extra = 0
    classes = ('grp-collapse', 'grp-open')


@admin.register(Cliente)
class PerfilEmpleadoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    search_fields = ('nombre', 'user__first_name', 'user__last_name', 'cedula', 'celular', 'user__email')
    list_display = ('user', 'cedula', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno')
    list_filter = ('entidad',)

    inlines = [beneficiarios_sepelio, beneficiarios_accidente]
    change_form_template = 'cotizador/admin/perfil.html'


class beneficiarios_sepelio_tabular(admin.TabularInline):
    model = benSepelio
    extra = 0
    classes = ('grp-collapse', 'grp-open')
    fields = ('parentesco', 'primer_nombre', 'segundo_nombre',
              'apellido_paterno', 'apellido_materno', 'fecha_nacimiento',
              'tipo_identificacion', 'file_cedula')
    readonly_fields = ('parentesco', 'primer_nombre', 'segundo_nombre',
                       'apellido_paterno', 'apellido_materno', 'fecha_nacimiento',
                       'tipo_identificacion', 'file_cedula')


class beneficiarios_accidente_tabular(admin.TabularInline):
    model = benAccidente
    extra = 0
    classes = ('grp-collapse', 'grp-open')
    fields = ('parentesco', 'primer_nombre', 'segundo_nombre',
              'apellido_paterno', 'apellido_materno', 'fecha_nacimiento',
              'tipo_identificacion', 'file_cedula')
    readonly_fields = ('parentesco', 'primer_nombre', 'segundo_nombre',
                       'apellido_paterno', 'apellido_materno', 'fecha_nacimiento',
                       'tipo_identificacion', 'file_cedula')


@admin.register(OrdenTrabajo)
class ordenTrabajoAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('nomeclatura', 'created', 'user', 'tipo')
    list_filter = ('tipo',)
    fields = ('tipo', 'user')
    readonly_fields = ('tipo', 'user')

    def get_inline_instances(self, request, obj=None):
        print(obj.tipo)
        if obj.tipo == 'CF':
            self.inlines = [beneficiarios_sepelio_tabular, ]
        if obj.tipo == 'AP':
            self.inlines = [beneficiarios_accidente_tabular, ]
        return super().get_inline_instances(request, obj=obj)

    actions = [reporte_inclusion, ]


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('marca', 'porcentaje_deducible', 'minimo', 'rotura_vidrios')
    search_fields = ('marca',)
    form = MarcaRecargoForm


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'celular', 'email_personal', 'contacto')


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    pass
