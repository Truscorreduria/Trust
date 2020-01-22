from django import forms
from .widgets import SelectSearch
from cotizador.models import PerfilEmpleado, Ticket, benAccidente, benSepelio


class LteTicketForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=PerfilEmpleado.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)

    class Meta:
        model = Ticket
        fields = '__all__'


class LteAccidentetForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=PerfilEmpleado.objects.all(), label='Titular',
                                      required=True, widget=SelectSearch)

    class Meta:
        model = benAccidente
        fields = '__all__'


class LteSepelioForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=PerfilEmpleado.objects.all(), label='Titular',
                                      required=True, widget=SelectSearch)

    class Meta:
        model = benSepelio
        fields = '__all__'
