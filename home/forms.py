from django import forms
from backend.models import Oportunity, TipoDoc


class OportunityForm(forms.ModelForm):
    tipo_seguro = forms.ChoiceField(choices=(), label="Tipo de Seguro")
    marca = forms.ChoiceField(choices=(), label="Marca")
    modelo = forms.ChoiceField(choices=(), label="Modelo")
    anno = forms.ChoiceField(choices=(), label="Año")

    tipo_doc = forms.ChoiceField(choices=TipoDoc.choices(), label="Tipo de ID")
    identificacion = forms.CharField(max_length=14, label="Identificación")
    primer_nombre = forms.CharField(max_length=125, label="Primer Nombre")
    segundo_nombre = forms.CharField(max_length=125, label="Segundo Nombre")
    apellido_paterno = forms.CharField(max_length=125, label="Primer Apellido")
    apellido_materno = forms.CharField(max_length=125, label="Segundo Apellido")
    celular = forms.CharField(max_length=8, label="Celular")
    email_personal = forms.EmailField(max_length=255, label="Correo Electrónico")

    class Meta:
        model = Oportunity
        fields = "__all__"
