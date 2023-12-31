from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()


class LoginView(AuthLoginView):
    authentication_form = LoginForm


app_name = 'cotizador'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('cotizar', cotizar, name='cotizar'),
    path('perfil/', perfil, name='perfil'),
    path('change_password/', change_password, name='change_password'),
    path('siniestros', siniestros, name='siniestros'),
    path('recomendados/', recomendados, name='recomendados'),
    path('misseguros', misseguros, name='misseguros'),
    path('solicitar_baja', solicitar_baja, name='solicitar_baja'),
    path('solicitar_baja_auto', solicitar_baja_auto, name='solicitar_baja_auto'),
    path('solicitud_renovacion_auto', solicitud_renovacion_auto, name='solicitud_renovacion_auto'),
    path('contactanos/', contactanos, name='contactanos'),
    path('get_data/', get_data, name='get_data'),
    path('get_modelos/', get_modelos, name='get_modelos'),
    path('get_annos/', get_annos, name='get_annos'),
    path('cotizacion_manual/', cotizacion_manual, name='cotizacion_manual'),
    path('guardar_poliza/', guardar_poliza, name='guardar_poliza'),
    path('generar_cotizacion/', generar_cotizacion, name='generar_cotizacion'),
    path('calcular_tabla_pagos/', calcular_tabla_pagos_polizas, name='calcular_tabla_pagos'),
    path('print_recibo/', print_recibo, name='print_recibo'),
    path('print_cotizacion/', print_cotizacion, name='print_cotizacion'),
    path('print_documentos/', print_documentos, name='print_documentos'),
    path('print_condiciones/', print_condiciones, name='print_condiciones'),
    path('print_orden_trabajo/', print_orden_trabajo, name='print_orden_trabajo'),
    path('print_orden_trabajo_sepelio/', print_orden_trabajo_sepelio, name='print_orden_trabajo_sepelio'),
    path('print_orden_trabajo_accidente/', print_orden_trabajo_accidente, name='print_orden_trabajo_accidente'),
    path('print_cesion/', print_cesion, name='print_cesion'),
    path('print_soa/', print_soa, name='print_soa'),
    path('enviar_contacto/', enviar_contacto, name='enviar_contacto'),
    path('admin_tasks/', admin_tasks, name='admin_tasks'),


    path('guardar_sepelio/', guardar_sepelio, name='guardar_sepelio'),
    path('costo_accidente/', costo_accidente, name='costo_accidente'),
    path('guardar_accidente/', guardar_accidente, name='guardar_accidente'),
    path('restablecer_password/', restablecer_password, name='restablecer_password'),
    path('invitacion/', invitacion, name='invitacion'),

    path('download/', download, name="download"),
    path('login/', LoginView.as_view(template_name='cotizador/login.html'), name="login"),
    path('logout/', LogoutView.as_view(next_page="/"), name="logout"),

    path('ingresar_numero_poliza', ingresar_numero_poliza, name="ingresar_numero_poliza"),
    path('javascript/<file>/', javascript, name="javascript"),
]
