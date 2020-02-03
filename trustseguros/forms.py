from django import forms
from .widgets import SelectSearch, TableBorderedInput, TableBordered
from cotizador.models import *


class ContactoForm(forms.ModelForm):
    prefix = 'cliente_contacto'

    class Meta:
        model = Contacto
        fields = ('nombre', 'cedula', 'telefono', 'celular', 'email_personal')


class ClienteJuridicioForm(forms.ModelForm):
    contactos = forms.Field(label="", required=False, widget=TableBorderedInput(
        attrs={
            'form': ContactoForm
        }
    ))
    tramites = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('code', 'Número'),
                ('poliza', 'Póliza'),
                ('prioridad', 'Prioridad'),
                ('created', 'Fecha del trámite'),
                ('vence', 'Fecha de vencimiento'),
                ('estado', 'Estado'),
            )
        }
    ))
    polizas = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('no_poliza', 'Número de póliza'),
                ('ramo', 'Ramo'),
                ('sub_ramo', 'Sub ramo'),
                ('fecha_vence', 'Fecha de vencimiento'),
            )
        }
    ))

    class Meta:
        model = ClienteJuridico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['contactos'] = instance.contactos()
            updated_initial['polizas'] = instance.polizas()
            updated_initial['tramites'] = instance.tramites()
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class ClienteNaturalForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(queryset=ClienteJuridico.objects.all(), required=False)
    tramites = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('code', 'Número'),
                ('poliza', 'Póliza'),
                ('prioridad', 'Prioridad'),
                ('created', 'Fecha del trámite'),
                ('vence', 'Fecha de vencimiento'),
                ('estado', 'Estado'),
            )
        }
    ))
    polizas = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('no_poliza', 'Número de póliza'),
                ('ramo', 'Ramo'),
                ('sub_ramo', 'Sub ramo'),
                ('suma_asegurada', 'Suma asegurada'),
                ('prima', 'Prima'),
                ('fecha_vence', 'Fecha de vencimiento'),
            )
        }
    ))

    class Meta:
        model = ClienteNatural
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['polizas'] = instance.polizas()
            updated_initial['tramites'] = instance.tramites()
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class CoberturaForm(forms.ModelForm):
    prefix = 'subramo_cobertura'

    class Meta:
        model = Cobertura
        fields = ('name', 'tipo_calculo', 'tipo_cobertura', 'tipo_exceso', 'iva')


class SubRamoForm(forms.ModelForm):
    coberturas = forms.Field(label='', required=False,
                             widget=TableBorderedInput(
                                 attrs={
                                     'form': CoberturaForm
                                 }
                             ))

    class Meta:
        model = SubRamo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['coberturas'] = instance.coberturas.all()
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)



class PolizaForm(forms.ModelForm):

    class Meta:
        model = Poliza
        fields = '__all__'


class LteTicketForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)

    class Meta:
        model = Ticket
        fields = '__all__'


class LteAccidentetForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Titular',
                                      required=True, widget=SelectSearch)

    class Meta:
        model = benAccidente
        fields = '__all__'


class LteSepelioForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Titular',
                                      required=True, widget=SelectSearch)

    class Meta:
        model = benSepelio
        fields = '__all__'
