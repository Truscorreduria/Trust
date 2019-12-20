from django.urls import path
from .views import *


app_name = 'migracion'

urlpatterns = [
    path('usuario_cotizador', usuario_cotizador, name="usuario_coctizador"),
]