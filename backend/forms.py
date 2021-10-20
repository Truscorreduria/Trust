from django import forms
from .models import *


class AseguradoraField(forms.ModelChoiceField):

    def __init__(self, queryset=Aseguradora.objects.all(), *, empty_label="---------",
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 **kwargs):
        super(AseguradoraField, self).__init__(queryset, empty_label="---------",
                                               required=True, widget=None, label=None, initial=None,
                                               help_text='', to_field_name=None, limit_choices_to=None,
                                               **kwargs)


class RamoField(forms.ModelChoiceField):

    def __init__(self, queryset=Ramo.objects.all(), *, empty_label="---------",
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 **kwargs):
        super(RamoField, self).__init__(queryset, empty_label="---------",
                                        required=True, widget=None, label=None, initial=None,
                                        help_text='', to_field_name=None, limit_choices_to=None,
                                        **kwargs)


class SubRamoField(forms.ModelChoiceField):

    def __init__(self, queryset=SubRamo.objects.all(), *, empty_label="---------",
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 **kwargs):
        super(SubRamoField, self).__init__(queryset, empty_label="---------",
                                           required=True, widget=None, label=None, initial=None,
                                           help_text='', to_field_name=None, limit_choices_to=None,
                                           **kwargs)


class ClienteField(forms.ModelChoiceField):

    def __init__(self, queryset=Cliente.objects.all(), *, empty_label="---------",
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 **kwargs):
        super(ClienteField, self).__init__(queryset, empty_label="---------",
                                           required=True, widget=None, label=None, initial=None,
                                           help_text='', to_field_name=None, limit_choices_to=None,
                                           **kwargs)


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="email", required=False)

    class Meta:
        model = Cliente
        fields = '__all__'


class ProspectoForm(forms.ModelForm):
    class Meta:
        model = ClienteProspecto
        fields = '__all__'


def _marcas():
    return [(m, m) for m in Referencia.objects.distinct('marca').values_list('marca', flat=True)]


class MarcaRecargoForm(forms.ModelForm):
    marca = forms.ChoiceField(choices=_marcas)

    class Meta:
        model = Marca
        fields = '__all__'


class InvitationForm(forms.Form):
    html = forms.CharField(widget=forms.Textarea)


class SoportesWidget(forms.Widget):
    template_name = 'backend/widgets/soportes.html'

    def format_value(self, value):
        if value:
            content_type = ContentType.objects.get(app_label=value._meta.app_label,
                                                   model=value._meta.model_name)
            return {
                'type': content_type,
                'pk': value.pk,
            }
        return {}


class PolizaForm(forms.ModelForm):
    media = forms.Field(label="Soportes", required=False,
                        widget=SoportesWidget())

    class Meta:
        model = Poliza
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.update(initial={
                'media': instance
            })
        super(PolizaForm, self).__init__(*args, **kwargs)
