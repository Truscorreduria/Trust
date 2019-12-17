from django.contrib import admin
from .models import *
from grappelli_extras.admin import entidad_admin
from import_export.admin import ImportExportModelAdmin


admin.site.register(Departamento, entidad_admin)

@admin.register(Municipio)
class municipioAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'departamento', 'active')
    list_filter = ('departamento', 'active')
    search_fields = ('name', 'departamento__name')
