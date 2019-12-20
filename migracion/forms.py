from .models import *
from django import forms
from .widgets import *


class FormEmpleado(forms.ModelForm):
    # automoviles = forms.CharField(label="Pólizas de automovil", widget=Automoviles)
    # accidentes = forms.CharField(label="Beneficiarios de accidente", widget=Accidentes)
    # sepelios = forms.CharField(label="Beneficiarios de sepelios", widget=Sepelios)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['automoviles'] = instance
            updated_initial['accidentes'] = instance
            updated_initial['sepelios'] = instance
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Empleado
        fields = '__all__'