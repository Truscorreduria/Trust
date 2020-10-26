from django.urls import path
from .views import *

app_name = "trustseguros"

urlpatterns = [
    path('', index, name="index"),
    path('profile/', profile, name="profile"),
    path('persona_natural/', PersonaNatural.as_view(), name="persona_natural"),
    path('persona_juridica/', PersonaJuridica.as_view(), name="persona_juridica"),
    path('lineas/', Lineas.as_view(), name="lineas"),
    path('campains/', Campains.as_view(), name="campains"),
    path('aseguradoras/', Aseguradoras.as_view(), name="aseguradoras"),
    path('tarifas/', Tarifas.as_view(), name="tarifas"),
    path('grupos/', Grupos.as_view(), name="grupos"),
    path('ramos/', Ramos.as_view(), name="ramos"),
    path('subramos/', SubRamos.as_view(), name="subramos"),
    path('polizas/', Polizas.as_view(), name="polizas"),
    path('tramites/', Tramites.as_view(), name="tramites"),
    path('configcotizador/', ConfiguracionCotizador.as_view(), name="configcotizador"),
    path('usuarios/', Usuarios.as_view(), name="usuarios"),
    path('oportunidades/<int:linea>/', Oportunidades.as_view(), name="oportunidades"),
    path('roles/', Roles.as_view(), name="roles"),
    path('documentos/', documentos, name="documentos"),
    path('comentarios/', comentarios, name="comentarios"),
    path('cobranza/', Recibos.as_view(), name="recibos"),
    path('siniestrotramite/', SiniestroTramite.as_view(), name="siniestrotramite"),
    path('siniestro/', Siniestros.as_view(), name="siniestro"),
    path('reporte_tramite/', ReporteTramite.as_view(), name="reporte_tramite"),
    path('reporte_poliza_emitida/', ReportePolizaEmitida.as_view(), name="reporte_poliza_emitida"),
    path('reporte_poliza_cancelada/', ReportePolizaCancelada.as_view(), name="reporte_poliza_cancelada"),
    path('reporte_poliza_renovada/', ReportePolizaRenovada.as_view(), name="reporte_poliza_renovada"),
    path('reporte_poliza_vencer/', ReportePolizaPorVencer.as_view(), name="reporte_poliza_vencer"),
    path('reporte_crm/', ReporteCRM.as_view(), name="reporte_crm"),
    path('reporte_siniestro/', ReporteSiniestro.as_view(), name="reporte_siniestro"),
    path('reporte_mora/', ReporteMora.as_view(), name="reporte_mora"),
    path('reporte_comision/', ReporteComision.as_view(), name="reporte_comision"),
]
