from django.urls import path
from .views import *


app_name = "trustseguros"


urlpatterns = [
    path('', index, name="index"),
    path('persona_natural/', PersonaNatural.as_view(), name="persona_natural"),
    path('persona_juridica/', PersonaJuridica.as_view(), name="persona_juridica"),
    path('prospectos/', Prospectos.as_view(), name="prospectos"),
    path('aseguradoras/', Aseguradoras.as_view(), name="aseguradoras"),
    path('grupos/', Grupos.as_view(), name="grupos"),
    path('ramos/', Ramos.as_view(), name="ramos"),
    path('subramos/', SubRamos.as_view(), name="subramos"),
    path('sepelio/', DependientesSepelio.as_view(), name="sepelio"),
    path('accidente/', DependientesAccidente.as_view(), name="accidente"),
    path('polizas/', PolizasAutomovil.as_view(), name="polizas"),
    path('tickets/', Tickets.as_view(), name="tickets"),
]
