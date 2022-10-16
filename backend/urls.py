from django.urls import path
from .views import *

app_name = "backend"

urlpatterns = [
    path('comentarios', Comentarios.as_view(), name='comentarios'),
]