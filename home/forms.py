from django import forms
from backend.models import TipoDoc, Referencia
from django.db.models import Count


class VehiculoForm(forms.Form):
    tipo_seguro = forms.ChoiceField(choices=(
        ('', '---------'),
        ('soa', 'Seguro obligatorio'),
        ('dap', 'Daños propios'),
    ), label="Tipo de Seguro")
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        marcas = Referencia.objects.values('marca').annotate(annos=Count('anno')).order_by('marca')
        marcas = [('', '---------')] + [(m['marca'], m['marca']) for m in marcas]
        self.fields['marca'].choices = marcas
        self.fields['identificacion'].widget.attrs['placeholder'] = 'Ej. 0010101010000A'
        self.fields['primer_nombre'].widget.attrs['placeholder'] = 'Ej. Carlos'
        self.fields['segundo_nombre'].widget.attrs['placeholder'] = 'Ej. Antonio'
        self.fields['apellido_paterno'].widget.attrs['placeholder'] = 'Ej. Aguilar'
        self.fields['apellido_materno'].widget.attrs['placeholder'] = 'Ej. Ruiz'
        self.fields['celular'].widget.attrs['placeholder'] = '88888888'
        self.fields['email_personal'].widget.attrs['placeholder'] = 'carlos@gmail.com'
        if self.data.get('marca'):
            annos = Referencia.objects.filter(marca=self.data.get('marca')).values('anno').annotate(
                Count('valor')).order_by('marca', 'anno')
            self.fields['anno'].choices = [(str(a['anno']), str(a['anno'])) for a in annos]
        if self.data.get('marca') and self.data.get('anno'):
            modelos = Referencia.objects.filter(marca=self.data.get('marca'), anno=self.data.get(
                'anno')).values('modelo').annotate(
                Count('valor')).order_by('marca', 'anno', 'modelo')
            self.fields['modelo'].choices = [(m['modelo'], m['modelo']) for m in modelos]


class AccidenteForm(forms.Form):
    tipo_doc = forms.ChoiceField(choices=TipoDoc.choices(), label="Tipo de ID")
    identificacion = forms.CharField(max_length=14, label="Identificación")
    primer_nombre = forms.CharField(max_length=125, label="Primer Nombre")
    segundo_nombre = forms.CharField(max_length=125, label="Segundo Nombre")
    apellido_paterno = forms.CharField(max_length=125, label="Primer Apellido")
    apellido_materno = forms.CharField(max_length=125, label="Segundo Apellido")
    celular = forms.CharField(max_length=8, label="Celular")
    email_personal = forms.EmailField(max_length=255, label="Correo Electrónico")
    profecion = forms.CharField(max_length=125, label="Profesión")
    ocupacion = forms.CharField(max_length=125, label="Ocupación")
    suma_asegurada = forms.ChoiceField(choices=(
        ("U$ 2,500.00", 2500.00),
        ("U$ 3,500.00", 3500.00),
    ), label="Suma Asegurada")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identificacion'].widget.attrs['placeholder'] = 'Ej. 0010101010000A'
        self.fields['primer_nombre'].widget.attrs['placeholder'] = 'Ej. Carlos'
        self.fields['segundo_nombre'].widget.attrs['placeholder'] = 'Ej. Antonio'
        self.fields['apellido_paterno'].widget.attrs['placeholder'] = 'Ej. Aguilar'
        self.fields['apellido_materno'].widget.attrs['placeholder'] = 'Ej. Ruiz'
        self.fields['celular'].widget.attrs['placeholder'] = '88888888'
        self.fields['email_personal'].widget.attrs['placeholder'] = 'carlos@gmail.com'
        self.fields['profecion'].widget.attrs['placeholder'] = 'Ej. Administración de Empresas'
        self.fields['ocupacion'].widget.attrs['placeholder'] = 'Ej. Analista Financiero'
