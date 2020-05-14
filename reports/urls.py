from django.urls import path
from .views import *

urlpatterns = [
    path('reporte_cotizacion_auto/', reporte_cotizacion_auto, name="reporte_cotizacion_auto"),
    path('reporte_debito_automatico/', reporte_debito_automatico, name="reporte_debito_automatico"),
    path('reporte_deduccion_nomina/', reporte_deduccion_nomina, name="reporte_deduccion_nomina"),
    path('reporte_polizas_vencer/', reporte_polizas_vencer, name="reporte_polizas_vencer"),
    path('reporte_renovaciones/', reporte_renovaciones, name="reporte_renovaciones"),
]
