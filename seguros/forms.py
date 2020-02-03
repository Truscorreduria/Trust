from django import forms
from .models import *


class SumaAseguradaWidget(forms.Widget):
    template_name = "seguros/widgets/sumaasegurada.html"

    def format_value(self, value):
        return value


class SumaAseguradaField(forms.Field):
    widget = SumaAseguradaWidget


class CoberturasAdicionalesWidget(forms.Widget):
    template_name = "seguros/widgets/coberturas_adicionales.html"

    def format_value(self, value):
        return value


class CoberturasAdicionalesField(forms.Field):
    widget = CoberturasAdicionalesWidget


class CotizacionForm(forms.ModelForm):
    marca = forms.ChoiceField(choices=marcas, required=False)
    modelo = forms.ChoiceField(choices=modelos, required=False)
    anno = forms.ChoiceField(choices=annos, required=False, label="Año")
    suma_asegurada = SumaAseguradaField(required=False)
    coberturas_adicionales = CoberturasAdicionalesField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['coberturas_adicionales'] = instance
            updated_initial['suma_asegurada'] = instance
        kwargs.update(initial=updated_initial)
        super(CotizacionForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Cotizacion
        fields = ('marca', 'modelo')

