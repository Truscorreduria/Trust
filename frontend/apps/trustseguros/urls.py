from django.urls import path
from .views import *

app_name = "trustseguros"

urlpatterns = [
    path('', index, name="index"),
    path('profile/', profile, name="profile"),
    path('reportes/', reportes, name="reportes"),
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
    path('siniestros/', Siniestros.as_view(), name="siniestros"),
    path('verificador/', verificador, name="verificador"),
]
