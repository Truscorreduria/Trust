from django.contrib import admin
from .forms import *
from import_export.admin import ImportExportModelAdmin
from grappelli_extras.admin import entidad_admin
from image_cropping.admin import ImageCroppingMixin

from django.contrib.admin import SimpleListFilter


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


class AseguradoraAdmin(ImageCroppingMixin, entidad_admin):
    fields = (('name', 'active'), ('emision', 'phone'), 'address', 'logo', 'cropping')
    list_display = ('name', 'phone', 'address', 'active')


admin.site.register(Aseguradora, AseguradoraAdmin)


class AntiguedadList(admin.TabularInline):
    model = Anno
    extra = 0
    classes = ('grp-collapse', 'grp-open')


class DepreciacionAdmin(admin.ModelAdmin):
    list_display = ('aseguradora', 'tipo_auto')
    list_filter = ('tipo_auto',)
    inlines = [AntiguedadList, ]
    save_as = True


admin.site.register(Depreciacion, DepreciacionAdmin)


class CoberturasList(admin.TabularInline):
    model = Cobertura
    extra = 0
    classes = ('grp-collapse', 'grp-open')


class ProductoAdmin(admin.ModelAdmin):
    fields = (('name', 'active'), 'description')
    change_form_template = 'seguros/producto.html'
    list_display = ('code', 'name', 'description', 'active')

    # inlines = [CoberturasList, ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['aseguradoras'] = Aseguradora.objects.filter(active=True)
        return super(ProductoAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


admin.site.register(Producto, ProductoAdmin)


class PrecioAdmin(admin.ModelAdmin):
    list_display = ('aseguradora', 'cobertura', 'valor')


# admin.site.register(Precio, PrecioAdmin)


class ReferenciaAdmin(ImportExportModelAdmin):
    list_display = ('marca', 'modelo', 'anno', 'valor', 'chasis')
    search_fields = ('marca', 'modelo')
    list_filter = ('marca', ModeloListFilter)


admin.site.register(Referencia, ReferenciaAdmin)


class Costos(admin.TabularInline):
    model = Costo
    extra = 0
    classes = ('grp-collapse', 'grp-open')
    fields = ('name', 'tipo_exceso', 'tipo_calculo', 'tasa', 'suma_asegurada', 'quota_seguro')
    readonly_fields = ('name', 'tipo_exceso', 'tipo_calculo', 'tasa', 'quota_seguro')


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('number', 'nombres', 'apellidos', 'email')

    form = CotizacionForm
    change_form_template = 'seguros/cotizacion.html'

    def get_fieldsets(self, request, obj=None):
        if obj and obj.id:
            return (('Datos Generales',
                     {'classes': ('grp-collapse grp-open',),
                      'fields': (('nombres', 'apellidos'), ('cedula', 'email'),
                                 ('chasis', 'motor'),
                                 ('marca', 'tipo_auto'), ('modelo', 'anno'),
                                 ('valor_nuevo', 'suma_asegurada'), 'coberturas_adicionales')
                      }),)
        else:
            return (('Por favor seleccione los siguientes datos',
                     {'classes': ('grp-collapse grp-open',),
                      'fields': (('producto', 'tipo_auto', 'aseguradora'),)
                      }),)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.id:
            return ('producto', 'aseguradora', 'number')
        else:
            return ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        aplicar_producto(obj.producto, obj)
        costos = [Costo.objects.get(id=int(x)) for x in request.POST.getlist('costo')]
        for c in costos:
            if c.tipo_exceso == 'otro':
                c.suma_asegurada = request.POST.get('suma_asegurada%s' % c.id)
                c.save()
            for a in obj.aseguradora.all():
                o, created = Oferta.objects.get_or_create(costo=c, aseguradora=a)
                o.quota_seguro = float(request.POST.get('%s' % o.id, 0.0))
                o.save()




                # class BanproAdmin(ImportExportModelAdmin):
                #     list_display = ('cedula', 'cliente', 'modelo', 'marca')
                #     search_fields = ('cedula', 'cliente')
                #     list_filter = ('marca', )
                #
                # admin.site.register(Banpro, BanproAdmin)
