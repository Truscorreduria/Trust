from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'seguros'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='seguros/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('grabar_cobertura/', grabar_cobertura, name="grabar_cobertura"),
    path('eliminar_cobertura/', eliminar_cobertura, name="eliminar_cobertura"),
    path('get_modelos/', get_modelos, name="get_modelos"),
    path('get_valor/', get_valor, name="get_valor"),
    path('suma_asegurada/', suma_asegurada, name="suma_asegurada"),
    path('generar_cotizacion/', generar_cotizacion, name="generar_cotizacion"),
]
