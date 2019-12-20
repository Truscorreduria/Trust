from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import FormEmpleado
from django.contrib.admin.filters import SimpleListFilter
from .views import generar_usuario


class NullFilterSpec(SimpleListFilter):
    title = u''

    parameter_name = u''

    def lookups(self, request, model_admin):
        return (
            ('1', 'Está lleno',),
            ('0', 'Está vacio',),
        )

    def queryset(self, request, queryset):
        kwargs = {
            '%s' % self.parameter_name: None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset


class EmpleadoNullFilter(NullFilterSpec):
    title = u'Empleado'
    parameter_name = u'empleado'


class TabularAuto(admin.TabularInline):
    model = Auto
    extra = 0
    classes = ('grp--collapse', 'grp-open')


class TabularSepelio(admin.TabularInline):
    model = Sepelio
    extra = 0
    classes = ('grp--collapse', 'grp-open')
    fields = (
    'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'parentesco', 'asegurado', 'cedula',
    'nacimiento')


class TabularAccidente(admin.TabularInline):
    model = Accidente
    extra = 0
    classes = ('grp--collapse', 'grp-open')
    fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'parentesco',
              'asegurado', 'cedula')


@admin.register(Empleado)
class EmpleadoAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'cedula', 'correo', 'username', '_username', 'nombres',
                    'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
                    'reversed', 'noblank')

    list_filter = ('nombres',)
    search_fields = ('cedula', 'name')
    form = FormEmpleado
    change_form_template = 'migracion/empleado_form.html'
    inlines = [TabularAuto, TabularSepelio, TabularAccidente]

    actions = ['generar_usuario_cotizador', ]

    def generar_usuario_cotizador(self, request, queryset):
        for q in queryset:
            generar_usuario(q, request)

@admin.register(Auto)
class AutoAdmin(ImportExportModelAdmin):
    list_display = ('contratante', 'empleado', '_empleado', 'marca', 'modelo', 'anno')
    # change_list_template = 'migracion/autolist.html'
    search_fields = ('contratante', 'marca', 'modelo', 'chasis', 'motor', 'poliza')
    list_filter = (EmpleadoNullFilter,)


@admin.register(Accidente)
class AutoAdmin(ImportExportModelAdmin):
    list_display = ('cedula', 'empleado', 'sugerencia', 'asegurado',
                    'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'parentesco', 'titular')
    list_filter = ('parentesco', 'nombres', EmpleadoNullFilter)
    search_fields = ('asegurado', 'cedula')

    # list_editable = ('asegurado', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido')
    class Media:
        js = ('migracion/js/sugerencia.js',)
        css = {
            'screen': ('migracion/css/list_editable.css',)
        }


@admin.register(Sepelio)
class AutoAdmin(ImportExportModelAdmin):
    list_display = ('asegurado', 'sugerencia', 'nacimiento', '_nacimiento', 'cedula', 'parentesco', 'inverted')
    search_fields = ('asegurado', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'ente')
    list_filter = ('nombres', 'parentesco', EmpleadoNullFilter)

    # list_editable = ('asegurado', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido')
    class Media:
        js = ('migracion/js/sugerencia.js',)
        css = {
            'screen': ('migracion/css/list_editable.css',)
        }


@admin.register(DependienteSepelio)
class Admin(ImportExportModelAdmin):
    list_display = (
    'id', 'nombre', 'certificado', 'ente', 'certificado_dependiente', 'nombre_dependiente', 'parentesco',
    'cedula', 'ente_dependiente', 'titular')
    search_fields = ('nombre', 'nombre_dependiente')
    list_filter = ('parentesco',)
