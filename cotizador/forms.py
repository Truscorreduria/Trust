from django import forms
from .models import *


class ProspectoForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'


class NaturalForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(queryset=ClienteJuridico.objects.all(), required=False)
    
    class Meta:
        model = ClienteNatural
        fields = '__all__'


def _marcas():
    return [(m, m) for m in Referencia.objects.distinct('marca').values_list('marca', flat=True)]


class MarcaRecargoForm(forms.ModelForm):
    marca = forms.ChoiceField(choices=_marcas)

    class Meta:
        model = Marca
        fields = '__all__'
