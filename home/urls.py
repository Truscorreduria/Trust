from django.conf.urls import url
from .views import *

app_name = 'home'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^lineas/', lineas, name='lineas'),
    url(r'^nosotros/', nosotros, name='nosotros'),
    url(r'^corredor/', corredor, name='corredor'),
    url(r'^plataformas/', plataformas, name='plataformas'),
    url(r'^politicas/', politicas, name='politicas'),
    url(r'^contacto/', contacto, name='contacto'),
    url(r'^cotiza_auto/', cotiza_auto, name='cotiza_auto'),
    url(r'^cotiza_api/', cotiza_api, name='cotiza_api'),
]
