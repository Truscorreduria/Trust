from django import forms
from .models import *
from .widgets import formaPago, listaPolizas, polizasGrupo, autoCompleteCliente
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.contrib.admin.widgets import AdminDateWidget
from .widgets import SelectSearch
from cotizador.models import PerfilEmpleado, Ticket, benAccidente, benSepelio

# region admin

class EndosoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(),
                                     widget=autoCompleteCliente())
    forma_pago = forms.CharField(required=True,
                                 widget=formaPago())
    cuotas = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['forma_pago'] = instance
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class ClienteForm(forms.ModelForm):
    ruc = forms.CharField(max_length=14, label="Número ruc")
    class Meta:
        model = Cliente
        fields = '__all__'

    lista_polizas = forms.CharField(required=False,
                                    widget=listaPolizas())

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['lista_polizas'] = instance
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class TramiteForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(),
                                     widget=autoCompleteCliente())


class PolizaForm(forms.ModelForm):
    lista_endosos = forms.CharField(required=False,
                                    widget=listaPolizas())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(),
                                     widget=autoCompleteCliente())

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['lista_endosos'] = instance
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class GrupoForm(forms.ModelForm):
    polizas_grupo = forms.CharField(required=False,
                                    widget=polizasGrupo())

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['polizas_grupo'] = instance
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class BeneficiarioForm(forms.ModelForm):
    cliente = forms.CharField(required=False,
                              widget=autoCompleteCliente())


class CertificadoForm(forms.ModelForm):
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(),
                                    widget=forms.HiddenInput)

    class Meta:
        model = Certificado
        fields = ('__all__')


class ImportEmpresaForm(forms.ModelForm):
    fecha_constitucion = forms.DateField(required=False, widget=AdminDateWidget(format='%Y-%m-%d'))

    class Meta:
        model = Cliente
        fields = (
            'tipo', 'razon_social', 'tipo_identificacion', 'numero_identificacion', 'fecha_constitucion',
            'actividad_economica', 'pagina_web', 'observaciones', 'departamento', 'municipio', 'direccion', 'telefono',
            'celular', 'email_principal', 'email_alterno',
        )

    def clean(self):

        try:
            numero_identificacion = self.cleaned_data['numero_identificacion']
            try:
                Cliente.objects.get(numero_identificacion=numero_identificacion)
                self._errors['numero_identificacion'] = self.error_class(
                    ["Ya existe un cliente con este número de indentificación"])
            except ObjectDoesNotExist:
                if len(numero_identificacion) != 14:
                    self._errors['numero_identificacion'] = self.error_class(
                        ["El numero de cédula debe tener 14 dígitos sin guiones."])
        except KeyError:
            self._errors['numero_identificacion'] = self.error_class(
                ["El número de identificación es requerido!"])

        return self.cleaned_data


class ImportPersonaForm(forms.ModelForm):
    vecimiento_documento = forms.DateField(required=False, widget=AdminDateWidget(format='%Y-%m-%d'))
    fecha_nacimiento = forms.DateField(required=False, widget=AdminDateWidget(format='%Y-%m-%d'))

    class Meta:
        model = Cliente
        fields = (
            'tipo', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'genero',
            'estado_civil',
            'numero_identificacion', 'fecha_nacimiento', 'estado_civil', 'ocupacion',
            'departamento', 'municipio', 'direccion', 'telefono', 'celular', 'email_principal', 'email_alterno',
            'email_alterno')

    def clean(self):

        try:
            numero_identificacion = self.cleaned_data['numero_identificacion']
            try:
                Cliente.objects.get(numero_identificacion=numero_identificacion)
                self._errors['numero_identificacion'] = self.error_class(
                    ["Ya existe un cliente con este número de indentificación"])
            except ObjectDoesNotExist:
                if len(numero_identificacion) != 14:
                    self._errors['numero_identificacion'] = self.error_class(
                        ["El numero de cédula debe tener 14 dígitos sin guiones."])
        except KeyError:
            self._errors['numero_identificacion'] = self.error_class(
                ["El número de identificación es requerido!"])

        return self.cleaned_data


class ImportPolizaForm(forms.ModelForm):
    numero_identificacion = forms.CharField(max_length=14, required=True)

    class Meta:
        model = Poliza
        fields = (
            'numero_poliza', 'sub_ramo', 'estado_poliza', 'aseguradora', 'fecha_expedicion', 'fecha_inicio', 'fecha_fin',
            'prima_neta', 'derecho_emision', 'recargo_descuento', 'iva', 'otros', 'prima_total', 'porcentaje_comision',
            'monto_comision', 'comision_agencia', 'monto_agencia', 'forma_pago', 'metodo_pago', 'banco',
            'numero_identificacion', 'cliente'
        )

    def clean(self):
        try:
            numero_identificacion = self.cleaned_data['numero_identificacion']
            try:
                self.cleaned_data['cliente'] = Cliente.objects.get(numero_identificacion=numero_identificacion)
            except ObjectDoesNotExist:
                self._errors['numero_identificacion'] = (
                    "El número de identificación no se encontró en el catálogo de clientes",)
        except KeyError:
            self._errors['numero_identificacion'] = (
                "El número de identificación es requerido!",)
        try:
            numero_poliza = self.cleaned_data['numero_poliza']
            Poliza.objects.get(numero_poliza=numero_poliza)
            self._errors['numero_poliza'] = self.error_class(
                ['Ya existe una póliza con el número %s' % numero_poliza])
        except ObjectDoesNotExist:
            pass

        return self.cleaned_data


class ImportCertificadoEdificioForm(forms.ModelForm):
    numero_poliza = forms.CharField(max_length=14, required=True)
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.filter(tipo=2), required=False)

    class Meta:
        model = Certificado
        fields = (
            'numero', 'tipo', 'suma_asegurada', 'ubicacion', 'numero_poliza', 'poliza'
        )

    def clean(self):
        try:
            numero_poliza = self.cleaned_data['numero_poliza']
            try:
                poliza = Poliza.objects.get(numero_poliza=numero_poliza)
                self.cleaned_data['poliza'] = poliza
                try:
                    numero = self.cleaned_data['numero']
                    Certificado.objects.get(numero=numero, poliza=poliza)
                    self._errors['numero'] = self.error_class(
                        ['Ya existe un certificado con el número %s' % numero])
                except ObjectDoesNotExist:
                    pass
            except ObjectDoesNotExist:
                self._errors['numero_poliza'] = (
                    "El número de póliza no se encontró en la base de datos",)
        except KeyError:
            self._errors['numero_poliza'] = (
                "El número de póliza es requerido!",)
        return self.cleaned_data


class ImportCertificadoAutoForm(forms.ModelForm):
    numero_poliza = forms.CharField(max_length=14, required=True)
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.filter(tipo=2), required=False)

    class Meta:
        model = Certificado
        fields = (
            'numero', 'tipo', 'numero_poliza', 'suma_asegurada', 'marca', 'modelo', 'placa', 'anno', 'motor', 'chasis',
            'poliza'
        )

    def clean(self):
        try:
            numero_poliza = self.cleaned_data['numero_poliza']
            try:
                poliza = Poliza.objects.get(numero_poliza=numero_poliza)
                self.cleaned_data['poliza'] = poliza
                try:
                    numero = self.cleaned_data['numero']
                    Certificado.objects.get(numero=numero, poliza=poliza)
                    self._errors['numero'] = self.error_class(
                        ['Ya existe un certificado con el número %s' % numero])
                except ObjectDoesNotExist:
                    pass
            except ObjectDoesNotExist:
                self._errors['numero_poliza'] = (
                    "El número de póliza no se encontró en la base de datos",)
        except KeyError:
            self._errors['numero_poliza'] = (
                "El número de póliza es requerido!",)
        return self.cleaned_data


class ImportCertificadoPersonaForm(forms.ModelForm):
    numero_poliza = forms.CharField(max_length=14, required=True)
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.filter(tipo=2), required=False)

    class Meta:
        model = Certificado
        fields = (
            'numero', 'tipo', 'suma_asegurada', 'primer_nombre', 'segundo_nombre', 'primer_apellido',
            'segundo_apellido', 'tipo_persona', 'parentesco', 'cedula', 'fecha_nacimiento', 'numero_poliza',
            'poliza'
        )

    def clean(self):
        try:
            numero_poliza = self.cleaned_data['numero_poliza']
            try:
                poliza = Poliza.objects.get(numero_poliza=numero_poliza)
                self.cleaned_data['poliza'] = poliza
                try:
                    numero = self.cleaned_data['numero']
                    Certificado.objects.get(numero=numero, poliza=poliza)
                    self._errors['numero'] = self.error_class(
                        ['Ya existe un certificado con el número %s' % numero])
                except ObjectDoesNotExist:
                    pass
            except ObjectDoesNotExist:
                self._errors['numero_poliza'] = (
                    "El número de póliza no se encontró en la base de datos",)
        except KeyError:
            self._errors['numero_poliza'] = (
                "El número de póliza es requerido!",)
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['tipo'] = 'persona'
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


# endregion


# region lte

class LtePolizaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)

    class Meta:
        model = Poliza
        fields = '__all__'


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

# endregion