from django.urls import path
from .views import *


app_name = "trustseguros"


urlpatterns = [
    path('', index, name="index"),
    path('usuarios/', Usuarios.as_view(), name="usuarios"),
    path('sepelio/', DependientesSepelio.as_view(), name="sepelio"),
    path('accidente/', DependientesAccidente.as_view(), name="accidente"),
    path('automovil/', PolizasAutomovil.as_view(), name="automovil"),
    path('tickets/', Tickets.as_view(), name="tickets"),

]
