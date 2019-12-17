from django import forms
from django.contrib.auth.models import User
from image_cropping import ImageCropWidget
from .models import Departamento, Municipio, Marca, Referencia
from datetime import datetime


class ProfileForm(forms.ModelForm):
    primer_nombre = forms.CharField(required=False)
    segundo_nombre = forms.CharField(required=False)
    apellido_paterno = forms.CharField(required=False)
    apellido_materno = forms.CharField(required=False)
    email_personal = forms.EmailField(required=False)
    celular = forms.CharField(required=False)
    cedula = forms.CharField(required=False, max_length=14)
    telefono = forms.CharField(required=False)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.filter(active=True))
    municipio = forms.ModelChoiceField(queryset=Municipio.objects.filter(active=True))
    domicilio = forms.CharField(required=False)
    sucursal = forms.CharField(required=False)
    codigo_empleado = forms.CharField(required=False)
    cargo = forms.CharField(required=False)
    foto = forms.ImageField(required=False, widget=ImageCropWidget)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance', None)
        initial_data = {}
        if user:
            perfil = user.profile()
            initial_data['celular'] = perfil.celular
            initial_data['cedula'] = perfil.cedula
            initial_data['telefono'] = perfil.telefono
            initial_data['domicilio'] = perfil.domicilio
            initial_data['sucursal'] = perfil.sucursal
            initial_data['codigo_empleado'] = perfil.codigo_empleado
            initial_data['cargo'] = perfil.cargo
        else:
            pass
        kwargs.update(initial=initial_data)
        super(ProfileForm, self).__init__(*args, **kwargs)


def _marcas():
    return [(m, m) for m in Referencia.objects.distinct('marca').values_list('marca', flat=True)]


class MarcaRecargoForm(forms.ModelForm):
    marca = forms.ChoiceField(choices=_marcas)
    class Meta:
        model = Marca
        fields = ('__all__')