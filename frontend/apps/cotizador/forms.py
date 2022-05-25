from backend.models import Recomendado
from django import forms
from django.core.validators import RegexValidator


class RecomendadoForm(forms.ModelForm):
    primer_nombre = forms.CharField(max_length=125)
    apellido_paterno = forms.CharField(max_length=125)
    celular = forms.CharField(max_length=8, validators=[RegexValidator('[0-9]{8,8}'), ])

    class Meta:
        model = Recomendado
        fields = '__all__'
