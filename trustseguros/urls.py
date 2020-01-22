from django.urls import path
from .views import *


app_name = "trustseguros"


urlpatterns = [
    path('', index, name="index"),
    path('persona_natural/', PersonaNatural.as_view(), name="persona_natural"),
    path('persona_juridica/', PersonaJuridica.as_view(), name="persona_juridica"),
    path('prospectos/', Prospectos.as_view(), name="prospectos"),
    path('sepelio/', DependientesSepelio.as_view(), name="sepelio"),
    path('accidente/', DependientesAccidente.as_view(), name="accidente"),
    path('automovil/', PolizasAutomovil.as_view(), name="automovil"),
    path('tickets/', Tickets.as_view(), name="tickets"),
]
