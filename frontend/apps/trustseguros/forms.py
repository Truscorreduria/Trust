from django import forms
from .widgets import *
from backend.models import *


class ContactoAseguradoraForm(forms.ModelForm):
    prefix = 'contacto_aseguradora'

    class Meta:
        model = ContactoAseguradora
        fields = ('name',)


class AseguradoraForm(forms.ModelForm):
    contactos = forms.Field(required=False, label="",
                            widget=TableBorderedInput(
                                attrs={
                                    'form': ContactoAseguradoraForm
                                }
                            ))

    class Meta:
        model = Aseguradora
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(initial={
                'contactos': instance.contactos()
            })
        super(AseguradoraForm, self).__init__(*args, **kwargs)


class ContactoForm(forms.ModelForm):
    prefix = 'cliente_contacto'

    telefono = forms.CharField(required=False, label="teléfono", widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))
    celular = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))

    class Meta:
        model = Contacto
        fields = ('nombre', 'cedula', 'telefono', 'celular', 'email_personal')


class RepresentanteForm(forms.ModelForm):
    prefix = 'cliente_representante'

    tipo_identificacion = forms.ChoiceField(choices=TipoDoc.choices(), required=True)

    cedula = forms.CharField(required=True, label="Número de identificación")

    telefono = forms.CharField(required=False, label="teléfono", widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))
    celular = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))
    domicilio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'rows': '4'
        }
    ))

    class Meta:
        model = ClienteNatural
        fields = ('primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno',
                  'tipo_identificacion', 'cedula', 'departamento', 'municipio', 'domicilio',
                  'telefono', 'celular')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if not instance:
            self.fields['primer_nombre'].widget.attrs['readonly'] = 'readonly'
            self.fields['segundo_nombre'].widget.attrs['readonly'] = 'readonly'
            self.fields['apellido_paterno'].widget.attrs['readonly'] = 'readonly'
            self.fields['apellido_materno'].widget.attrs['readonly'] = 'readonly'
            self.fields['telefono'].widget.attrs['readonly'] = 'readonly'
            self.fields['celular'].widget.attrs['readonly'] = 'readonly'
            self.fields['domicilio'].widget.attrs['readonly'] = 'readonly'
            self.fields['departamento'].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio'].widget.attrs['disabled'] = 'disabled'
            self.fields['tipo_identificacion'].required = True
        else:
            self.fields['tipo_identificacion'].required = False
            self.fields['tipo_identificacion'].widget.attrs['disabled'] = 'disabled'
            self.fields['cedula'].widget.attrs['readonly'] = 'readonly'


class ClienteJuridicioForm(forms.ModelForm):
    razon_social = forms.CharField(required=True)
    ruc = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': 'A9{13,13}'
        }
    ))
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
                ('aseguradora.name', 'Aseguradora'),
                ('ramo', 'Ramo'),
                ('fecha_emision', 'Fecha inicio'),
                ('fecha_vence', 'Fecha fin'),
                ('dias_vigencia', 'Vence'),
                ('grupo', 'Grupo'),
                ('suma_asegurada', 'Suma asegurada'),
                ('total', 'Prima neta'),
                ('tipo_poliza', 'Tipo póliza'),
                ('estado', 'Estado'),
                ('ver', ''),
            )
        }
    ))
    telefono = forms.CharField(required=False, label="teléfono", widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))
    domicilio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'rows': '4'
        }
    ))

    representante = forms.ModelChoiceField(queryset=ClienteNatural.objects.all(), label="",
                                           required=False, widget=RepresentanteLegalWidget(
            attrs={
                'form': RepresentanteForm
            }
        ))

    class Meta:
        model = ClienteJuridico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClienteJuridicioForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['contactos'] = instance.contactos()
            updated_initial['polizas'] = instance.polizas()
            updated_initial['tramites'] = instance.tramites()
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)

    def clean_ruc(self):
        data = self.cleaned_data['ruc']
        if self.instance:
            if ClienteJuridico.objects.filter(ruc=data).exclude(id=self.instance.id).count() > 0:
                raise forms.ValidationError("Ya existe otro cliente con esta identificación!")
        else:
            if ClienteJuridico.objects.filter(ruc=data).count() > 0:
                raise forms.ValidationError("Ya existe otro cliente con esta identificación!")
        return data


class ClienteNaturalForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(queryset=ClienteJuridico.objects.all(), required=False)
    primer_nombre = forms.CharField(required=True)
    apellido_paterno = forms.CharField(required=True)
    genero = forms.ChoiceField(required=True, choices=GeneroCliente.choices())
    estado_civil = forms.ChoiceField(required=True, choices=EstadoCivil.choices())
    departamento = forms.ModelChoiceField(required=True, queryset=Departamento.objects.all())
    municipio = forms.ModelChoiceField(required=True, queryset=Municipio.objects.all())
    cedula = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{13,13}A'
        }
    ), label="Número de identificación")
    telefono = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))
    celular = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'inputmask',
            'data-mask': '9{8,8}'
        }
    ))
    domicilio = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'rows': '4'
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
                ('aseguradora.name', 'Aseguradora'),
                ('ramo', 'Ramo'),
                ('fecha_emision', 'Fecha inicio'),
                ('fecha_vence', 'Fecha fin'),
                ('dias_vigencia', 'Vence'),
                ('grupo', 'Grupo'),
                ('suma_asegurada', 'Suma asegurada'),
                ('total', 'Prima neta'),
                ('tipo_poliza', 'Tipo póliza'),
                ('estado', 'Estado'),
                ('ver', ''),
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

    def clean_cedula(self):
        data = self.cleaned_data['cedula']
        if self.instance:
            if ClienteNatural.objects.filter(cedula=data).exclude(id=self.instance.id).count() > 0:
                raise forms.ValidationError("Ya existe otro cliente con esta identificación!")
        else:
            if ClienteNatural.objects.filter(cedula=data).count() > 0:
                raise forms.ValidationError("Ya existe otro cliente con esta identificación!")
        return data


class CoberturaForm(forms.ModelForm):
    prefix = 'subramo_cobertura'

    class Meta:
        model = Cobertura
        fields = ('name', 'tipo_calculo', 'tipo_cobertura', 'tipo_exceso')


class CampoAdicionalForm(forms.ModelForm):
    prefix = 'ramo_campo_adicional'

    class Meta:
        model = CampoAdicional
        fields = ('name', 'label',)


class RamoForm(forms.ModelForm):
    class Meta:
        model = Ramo
        fields = '__all__'


class SubRamoForm(forms.ModelForm):
    coberturas = forms.Field(label='', required=False,
                             widget=TableBorderedInput(
                                 attrs={
                                     'form': CoberturaForm
                                 }
                             ))
    campos_adicionales = forms.Field(label='', required=False,
                                     widget=TableBorderedInput(
                                         attrs={
                                             'form': CampoAdicionalForm
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
            updated_initial['campos_adicionales'] = instance.datos_tecnicos.all()
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)


class PolizaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
    contratante = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Contratante',
                                         required=True, widget=SelectSearch)
    cesioinario = forms.ModelChoiceField(queryset=ClienteJuridico.objects.filter(es_cesionario=True),
                                         required=False, label="Cesionario")
    coberturas = forms.Field(label="", required=False, widget=CoberturasWidget)
    tabla_pagos = forms.Field(label="", required=False, widget=TablaPagosWidget)
    amount_comision = forms.FloatField(label="Total comisión", required=False, widget=forms.NumberInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    total = forms.FloatField(label="Total", required=False, initial=0.0,
                             widget=forms.NumberInput(
                                 attrs={
                                     'readonly': 'readonly'
                                 }
                             ))
    campos_adicionales = forms.Field(label="", required=False, widget=CamposAdicionalesWidget)
    drive = forms.Field(label="", required=False, widget=DriveWidget)
    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)

    estado_poliza = forms.ChoiceField(choices=EstadoPoliza.choices(), label="Estado póliza",
                                      required=False,
                                      widget=forms.Select(
                                          attrs={
                                              'disabled': 'disabled'
                                          }
                                      ))
    no_poliza = forms.CharField(max_length=50, required=True, label="Número de póliza")

    moneda = forms.ModelChoiceField(queryset=Moneda.objects.all().order_by('moneda'), required=False,
                                    widget=forms.Select(
                                        attrs={
                                            'style': "min-width: 178px"
                                        }
                                    ))
    pedir_comentarios = forms.Field(required=False,
                                    widget=PedirComentarioWidget)

    class Meta:
        model = Poliza
        exclude = ('editable', 'pedir_comentarios')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['campos_adicionales'] = instance
            updated_initial['fecha_vence'] = instance.fecha_vence.strftime('%d/%m/%Y')
            updated_initial['coberturas'] = instance
            updated_initial['tabla_pagos'] = instance
            updated_initial['drive'] = instance
            updated_initial['bitacora'] = instance
            updated_initial['pedir_comentarios'] = instance.perdir_comentarios
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)
        if instance and not instance.editable:
            self.fields['no_poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['no_recibo'].widget.attrs['readonly'] = 'readonly'
            self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
            self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
            self.fields['emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['iva'].widget.attrs['readonly'] = 'readonly'
            self.fields['otros'].widget.attrs['readonly'] = 'readonly'
            self.fields['total'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['suma_asegurada'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_vence'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['ramo'].widget.attrs['disabled'] = 'disabled'
            self.fields['sub_ramo'].widget.attrs['disabled'] = 'disabled'
            self.fields['aseguradora'].widget.attrs['disabled'] = 'disabled'
            self.fields['cliente'].widget.attrs['disabled'] = 'disabled'
            self.fields['contratante'].widget.attrs['disabled'] = 'disabled'
            self.fields['grupo'].widget.attrs['disabled'] = 'disabled'
            self.fields['tipo_poliza'].widget.attrs['disabled'] = 'disabled'
            self.fields['cesion_derecho'].widget.attrs['disabled'] = 'disabled'
            self.fields['cesioinario'].widget.attrs['disabled'] = 'disabled'
            self.fields['moneda'].widget.attrs['disabled'] = 'disabled'
            self.fields['f_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['m_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['cuotas'].widget.attrs['disabled'] = 'disabled'
            self.fields['concepto'].widget.attrs['disabled'] = 'disabled'
        if instance:
            if instance.f_pago == FormaPago.CONTADO:
                self.fields['cuotas'].widget.attrs['readonly'] = 'readonly'
        if instance and (instance.estado_poliza == EstadoPoliza.CANCELADA
                         or instance.estado_poliza == EstadoPoliza.ANULADA):
            self.fields['tipo_poliza'].required = False
            self.fields['cliente'].required = False
            self.fields['contratante'].required = False
        if instance and not instance.estado_poliza == EstadoPoliza.PENDIENTE:
            self.fields['moneda'].widget.attrs['disabled'] = 'disabled'
            self.fields['f_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['m_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['cuotas'].widget.attrs['disabled'] = 'disabled'
            self.fields['fecha_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
            self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
            self.fields['emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['iva'].widget.attrs['readonly'] = 'readonly'
            self.fields['otros'].widget.attrs['readonly'] = 'readonly'
            self.fields['total'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'


    # def clean(self):
    #     if not self.cleaned_data['total'] == self.cleaned_data['total_pagos']:
    #         raise forms.ValidationError("La suma de pagos y el total de la póliza no son iguales")
    #     return self.cleaned_data


class DatoImportForm(forms.ModelForm):
    extra_data = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = DatoPoliza
        fields = '__all__'


class TramiteForm(forms.ModelForm):
    code = forms.CharField(required=False, label="Número trámite", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly',
        }
    ))

    fecha = forms.CharField(required=False, label="Fecha registro", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    hora = forms.CharField(required=False, label="Hora registro", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    ramo = forms.CharField(required=False, label="Ramo", widget=ReadOnlyWidget)
    sub_ramo = forms.CharField(required=False, label="Sub ramo", widget=ReadOnlyWidget)
    grupo = forms.CharField(required=False, label="Grupo", widget=ReadOnlyWidget)
    aseguradora = forms.CharField(required=False, label="Aseguradora", widget=ReadOnlyWidget)
    descripcion = forms.CharField(widget=forms.Textarea(
        attrs={
            'rows': 4
        }
    ))

    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
    drive = forms.Field(label="", required=False, widget=DriveWidget)
    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)
    tabla_pagos = forms.Field(label="", required=False, widget=TablaPagosWidget)
    amount_comision = forms.FloatField(label="Total comisión", required=False, widget=forms.NumberInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    total = forms.FloatField(label="Total", required=False, initial=0.0,
                             widget=forms.NumberInput(
                                 attrs={
                                     'readonly': 'readonly'
                                 }
                             ))

    class Meta:
        model = Tramite
        exclude = ('editable',)

    @staticmethod
    def get_contacto_choices(poliza):
        return [(i.id, i.name) for i in ContactoAseguradora.objects.filter(aseguradora=poliza.aseguradora)]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['campos_adicionales'] = instance
            updated_initial['fecha'] = instance.created.strftime('%d/%m/%Y')
            updated_initial['hora'] = instance.created.strftime('%H:%M')
            updated_initial['drive'] = instance
            updated_initial['bitacora'] = instance
            updated_initial['tabla_pagos'] = instance
            if instance.poliza:
                updated_initial['aseguradora'] = instance.poliza.aseguradora
                updated_initial['grupo'] = instance.poliza.grupo
                updated_initial['ramo'] = instance.poliza.ramo
                updated_initial['sub_ramo'] = instance.poliza.sub_ramo
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)
        self.fields['contacto_aseguradora'].widget.choices = []
        if instance and not instance.editable:
            self.fields['cliente'].widget.attrs['disabled'] = 'disabled'
            self.fields['cliente'].required = False
            self.fields['tipo_tramite'].widget.attrs['disabled'] = 'disabled'
            self.fields['tipo_tramite'].required = False
            self.fields['poliza'].widget.attrs['disabled'] = 'disabled'
            self.fields['contacto_aseguradora'].widget.attrs['disabled'] = 'disabled'
            self.fields['solicitado_por'].widget.attrs['disabled'] = 'disabled'
            self.fields['medio_solicitud'].widget.attrs['disabled'] = 'disabled'
            self.fields['estado'].widget.attrs['disabled'] = 'disabled'
            self.fields['genera_endoso'].widget.attrs['disabled'] = 'disabled'
            self.fields['genera_endoso'].required = False
            self.fields['user'].widget.attrs['disabled'] = 'disabled'
            self.fields['descripcion'].widget.attrs['readonly'] = 'readonly'
            self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
            self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
            self.fields['emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['iva'].widget.attrs['readonly'] = 'readonly'
            self.fields['otros'].widget.attrs['readonly'] = 'readonly'
            self.fields['total'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['suma_asegurada'].widget.attrs['readonly'] = 'readonly'
            self.fields['moneda'].widget.attrs['disabled'] = 'disabled'
            self.fields['f_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['m_pago'].widget.attrs['disabled'] = 'disabled'
            self.fields['cuotas'].widget.attrs['disabled'] = 'disabled'
            self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
        if instance and instance.poliza:
            self.fields['contacto_aseguradora'].widget.choices = self.get_contacto_choices(instance.poliza)


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
