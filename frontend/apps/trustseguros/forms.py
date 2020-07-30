from django import forms
from .widgets import *
from backend.models import *


class LteFormMixing:

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')


class ContactoAseguradoraForm(forms.ModelForm):
    prefix = 'contacto_aseguradora'

    class Meta:
        model = ContactoAseguradora
        fields = ('name',)


class ValorDepreciacion(forms.ModelForm):
    class Meta:
        model = Anno
        fields = ('antiguedad', 'factor')


class AseguradoraForm(forms.ModelForm):
    address = forms.CharField(required=False, label="", widget=forms.Textarea(
        attrs={
            'rows': 4
        }
    ))

    depreciacion = forms.Field(required=False, label="",
                               widget=TableBorderedInput(
                                   attrs={
                                       'form': ValorDepreciacion
                                   }
                               ))

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
                'contactos': instance.contactos(),
                'depreciacion': instance.depreciacion()
            })
        super(AseguradoraForm, self).__init__(*args, **kwargs)


class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = '__all__'


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
        fields = (
            'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'cedula', 'telefono', 'celular',
            'email_personal')


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
        instance = kwargs.get('instance', None)
        request = kwargs.pop('request', None)
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
                ('aseguradora', 'Aseguradora'),
                ('ramo', 'Ramo'),
                ('fecha_emision', 'Fecha inicio'),
                ('fecha_vence', 'Fecha fin'),
                ('dias_vigencia', 'Vence'),
                ('grupo', 'Grupo'),
                ('suma_asegurada', 'Suma asegurada'),
                ('total', 'Prima neta'),
                ('tipo_poliza_display', 'Tipo póliza'),
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
        instance = kwargs.get('instance', None)
        request = kwargs.pop('request', None)
        super(ClienteJuridicioForm, self).__init__(*args, **kwargs)
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
                ('aseguradora', 'Aseguradora'),
                ('ramo', 'Ramo'),
                ('fecha_emision', 'Fecha inicio'),
                ('fecha_vence', 'Fecha fin'),
                ('dias_vigencia', 'Vence'),
                ('grupo', 'Grupo'),
                ('suma_asegurada', 'Suma asegurada'),
                ('total', 'Prima neta'),
                ('tipo_poliza_display', 'Tipo póliza'),
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
        request = kwargs.pop('request', None)
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
        fields = ('name', 'en_cotizacion')


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
                             widget=CoberturaSubRamoWidget(
                                 attrs={
                                     'form': CoberturaForm,
                                     'columns': ('name', 'en_cotizacion'),
                                     'aseguradoras': Aseguradora.objects.all()
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

    prima_total = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ), initial=0.0)
    saldo_pendiente = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ), initial=0.0)

    class Meta:
        model = Poliza
        fields = (
            'no_poliza', 'ramo', 'sub_ramo', 'fecha_emision', 'fecha_vence', 'aseguradora',
            'cliente', 'contratante', 'grupo', 'tipo_poliza', 'cesion_derecho', 'cesioinario',
            'estado_poliza', 'no_recibo', 'concepto', 'pedir_comentarios', 'coberturas',
            'f_pago', 'm_pago', 'cuotas', 'fecha_pago', 'subtotal', 'descuento',
            'emision', 'iva', 'otros', 'total', 'per_comision', 'suma_asegurada',
            'amount_comision', 'moneda', 'tabla_pagos', 'campos_adicionales', 'drive', 'bitacora',
        )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['campos_adicionales'] = instance
            try:
                updated_initial['fecha_vence'] = instance.fecha_vence.strftime('%d/%m/%Y')
            except AttributeError:
                pass
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
            self.fields['fecha_emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_vence'].widget.attrs['readonly'] = 'readonly'
            self.fields['ramo'].widget.attrs['readonly'] = 'readonly'
            self.fields['sub_ramo'].widget.attrs['readonly'] = 'readonly'
            self.fields['aseguradora'].widget.attrs['readonly'] = 'readonly'
            self.fields['cliente'].widget.attrs['disabled'] = 'disabled'
            self.fields['contratante'].widget.attrs['disabled'] = 'disabled'
            self.fields['grupo'].widget.attrs['readonly'] = 'readonly'
            self.fields['tipo_poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['cesion_derecho'].widget.attrs['readonly'] = 'readonly'
            self.fields['cesioinario'].widget.attrs['readonly'] = 'readonly'
            self.fields['concepto'].widget.attrs['readonly'] = 'readonly'
        if instance:
            if instance.f_pago == FormaPago.CONTADO:
                self.fields['cuotas'].widget.attrs['readonly'] = 'readonly'
        if instance and (instance.estado_poliza == EstadoPoliza.CANCELADA
                         or instance.estado_poliza == EstadoPoliza.ANULADA):
            self.fields['tipo_poliza'].required = False
            self.fields['cliente'].required = False
            self.fields['contratante'].required = False
        if instance and not instance.estado_poliza == EstadoPoliza.PENDIENTE:
            self.fields['moneda'].widget.attrs['readonly'] = 'readonly'
            self.fields['f_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['m_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['cuotas'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
            self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
            self.fields['emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['iva'].widget.attrs['readonly'] = 'readonly'
            self.fields['otros'].widget.attrs['readonly'] = 'readonly'
            self.fields['total'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'


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
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(), required=False,
                                    widget=forms.Select(
                                        choices=[]
                                    ))

    class Meta:
        model = Tramite
        exclude = ('editable',)

    @staticmethod
    def get_contacto_choices(poliza):
        choices = [(None, '---------')]
        for i in ContactoAseguradora.objects.filter(aseguradora=poliza.aseguradora):
            choices.append((i.id, i.name))
        return choices

    @staticmethod
    def get_poliza_choices(cliente):
        choices = [(None, '---------')]
        for i in Poliza.objects.filter(cliente=cliente, estado_poliza=EstadoPoliza.ACTIVA):
            choices.append((i.id, i.no_poliza))
        return choices

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        request = kwargs.pop('request', None)
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
        else:
            if request:
                updated_initial['user'] = request.user
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)
        self.fields['contacto_aseguradora'].choices = []
        self.fields['poliza'].choices = []
        if instance and instance.cliente:
            self.fields['poliza'].choices = self.get_poliza_choices(instance.cliente)
        if instance and instance.poliza:
            self.fields['contacto_aseguradora'].widget.choices = self.get_contacto_choices(instance.poliza)
        if instance and (instance.estado == 'Finalizado' or instance.estado == 'Anulado'):
            self.fields['tipo_tramite'].widget.attrs['readonly'] = 'readonly'
            self.fields['contacto_aseguradora'].widget.attrs['readonly'] = 'readonly'
            self.fields['solicitado_por'].widget.attrs['readonly'] = 'readonly'
            self.fields['medio_solicitud'].widget.attrs['readonly'] = 'readonly'
            self.fields['estado'].widget.attrs['readonly'] = 'readonly'
            self.fields['genera_endoso'].widget.attrs['readonly'] = 'readonly'
            self.fields['user'].widget.attrs['readonly'] = 'readonly'
            self.fields['descripcion'].widget.attrs['readonly'] = 'readonly'
            self.fields['f_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['m_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['cuotas'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
            self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
            self.fields['emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['iva'].widget.attrs['readonly'] = 'readonly'
            self.fields['otros'].widget.attrs['readonly'] = 'readonly'
            self.fields['total'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['moneda'].widget.attrs['readonly'] = 'readonly'
            self.fields['poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['cliente'].widget.attrs['disabled'] = 'disabled'


class FieldMapForm(forms.ModelForm):
    origin_field = forms.CharField(widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ))

    class Meta:
        model = FieldMap
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.fields['destiny_field'].queryset = CampoAdicional.objects.filter(id=0)
        if instance and instance.fieldmap_type == FieldMapType.AUTOMOVIL:
            self.fields['destiny_field'].queryset = CampoAdicional.objects.filter(
                sub_ramo=instance.config.sub_ramo_automovil)
        if instance and instance.fieldmap_type == FieldMapType.SEPELIO:
            self.fields['destiny_field'].queryset = CampoAdicional.objects.filter(
                sub_ramo=instance.config.sub_ramo_sepelio)
        if instance and instance.fieldmap_type == FieldMapType.ACCIDENTE:
            self.fields['destiny_field'].queryset = CampoAdicional.objects.filter(
                sub_ramo=instance.config.sub_ramo_accidente)


class CotizadorConfigForm(forms.ModelForm):
    fieldmap_automovil = forms.Field(required=False, label="",
                                     widget=FieldMapWidget(
                                         attrs={
                                             'origin_columns': ('marca', 'modelo', 'anno', 'chasis', 'motor',
                                                                'placa', 'color',),
                                             'type': FieldMapType.AUTOMOVIL,
                                             'form': FieldMapForm
                                         }
                                     ))
    fieldmap_sepelio = forms.Field(required=False, label="",
                                   widget=FieldMapWidget(
                                       attrs={
                                           'origin_columns': ('primer_nombre', 'segundo_nombre', 'apellido_paterno',
                                                              'apellido_materno', 'costo', 'suma_asegurada',
                                                              'tipo_identificacion', 'fecha_nacimiento',),
                                           'type': FieldMapType.SEPELIO,
                                           'form': FieldMapForm
                                       }
                                   ))
    fieldmap_accidente = forms.Field(required=False, label="",
                                     widget=FieldMapWidget(
                                         attrs={
                                             'origin_columns': ('primer_nombre', 'segundo_nombre', 'apellido_paterno',
                                                                'apellido_materno', 'costo', 'suma_asegurada',
                                                                'tipo_identificacion', 'fecha_nacimiento',),
                                             'type': FieldMapType.ACCIDENTE,
                                             'form': FieldMapForm
                                         }
                                     ))

    class Meta:
        model = CotizadorConfig
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(
                initial={
                    'fieldmap_automovil': instance,
                    'fieldmap_sepelio': instance,
                    'fieldmap_accidente': instance,
                }
            )
        super().__init__(*args, **kwargs)


class ReportTramiteForm(forms.Form):
    estado = forms.ChoiceField(choices=EstadoTramite.choices(), required=False)
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False,
                                     widget=SelectSearch)
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(), required=False,
                                    widget=SelectSearch)


class UserForm(forms.ModelForm):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    lineas = forms.Field(label="líneas de negocio autorizadas", widget=LineaWidget, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(initial={
                'lineas': instance
            })
        super().__init__(*args, **kwargs)


class ProspectForm(forms.ModelForm):
    cedula = forms.CharField(required=True, label="Cédula")
    domicilio = forms.CharField(label="Dirección", required=False, widget=forms.Textarea(
        attrs={
            'rows': '4',
        }
    ))

    class Meta:
        model = Prospect
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if not instance:
            self.fields['primer_nombre'].widget.attrs['readonly'] = 'readonly'
            self.fields['segundo_nombre'].widget.attrs['readonly'] = 'readonly'
            self.fields['apellido_paterno'].widget.attrs['readonly'] = 'readonly'
            self.fields['apellido_materno'].widget.attrs['readonly'] = 'readonly'
            self.fields['telefono'].widget.attrs['readonly'] = 'readonly'
            self.fields['celular'].widget.attrs['readonly'] = 'readonly'
            self.fields['domicilio'].widget.attrs['readonly'] = 'readonly'
            self.fields['departamento'].widget.attrs['readonly'] = 'readonly'
            self.fields['municipio'].widget.attrs['readonly'] = 'readonly'
            self.fields['genero'].widget.attrs['readonly'] = 'readonly'
            self.fields['estado_civil'].widget.attrs['readonly'] = 'readonly'
            self.fields['email_personal'].widget.attrs['readonly'] = 'readonly'
        else:
            self.fields['cedula'].widget.attrs['readonly'] = 'readonly'


class OportunityForm(forms.ModelForm):
    status = forms.Field(widget=OportunityStatusWidget, label="", initial=OportunityStatus.PENDIENTE)
    days = forms.CharField(label="Dias transcurridos", required=False, widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    prospect = forms.ModelChoiceField(queryset=Prospect.objects.all(), label="", required=False, widget=FormWidget(
        attrs={
            'form': ProspectForm,
            'fields': (
                ('cedula', 'email_personal'),
                ('primer_nombre', 'segundo_nombre'),
                ('apellido_paterno', 'apellido_materno'),
                ('telefono', 'celular'),
                ('genero', 'estado_civil'),
                ('departamento', 'municipio'),
                ('domicilio',),
            ),
            'primary_key': 'cedula'
        }
    ))

    drive = forms.Field(label="", required=False, widget=DriveWidget)
    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)

    extra_data = forms.Field(label="", required=False, widget=JsonWidget)

    cotizacion = forms.Field(label="", required=False, widget=CotizacionWidget(
        attrs={
            'companies': Aseguradora.objects.filter(active=True),
            'instance': None,
        }
    ))
    code = forms.CharField(widget=forms.HiddenInput, required=False)
    vendedor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = Oportunity
        exclude = ('linea',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(
                initial={
                    'extra_data': instance,
                    'prospect': instance.prospect,
                    'drive': instance,
                    'bitacora': instance,
                    'days': instance.dias,
                }
            )
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['cotizacion'].widget.attrs['instance'] = instance


class LineaForm(forms.ModelForm):
    class Meta:
        model = Linea
        fields = '__all__'


class CampainForm(forms.ModelForm):
    class Meta:
        model = Campain
        fields = '__all__'


class ImportDataForm(forms.ModelForm):
    prefix = 'import'

    campain = forms.ModelChoiceField(queryset=Campain.objects.filter(active=True))
    vendedor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = Oportunity
        fields = ('campain', 'ramo', 'sub_ramo', 'vendedor',)


class PagoForm(forms.ModelForm):
    nombre_cliente = forms.CharField(label="Nombre del cliente", required=False,
                                     widget=forms.TextInput(
                                         attrs={
                                             'readonly': 'readonly'
                                         }
                                     ))
    numero_poliza = forms.CharField(label="Número de póliza", required=False,
                                    widget=forms.TextInput(
                                        attrs={
                                            'readonly': 'readonly'
                                        }
                                    ))
    aseguradora = forms.CharField(label="Aseguradora", required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'readonly': 'readonly'
                                      }
                                  ))
    numero_recibo = forms.CharField(label="Número de recibo", required=False,
                                    widget=forms.TextInput(
                                        attrs={
                                            'readonly': 'readonly'
                                        }
                                    ))
    fecha_vence = forms.CharField(label="Fecha de vencimiento", required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'readonly': 'readonly'
                                      }
                                  ))
    numero = forms.IntegerField(label="Número de cuota", required=False,
                                widget=forms.NumberInput(
                                    attrs={
                                        'readonly': 'readonly'
                                    }
                                ))
    monto = forms.FloatField(label="Valor a pagar", required=False,
                             widget=forms.NumberInput(
                                 attrs={
                                     'readonly': 'readonly'
                                 }
                             ))

    class Meta:
        model = Pago
        fields = ('nombre_cliente', 'numero_poliza', 'aseguradora', 'numero_recibo',
                  'fecha_vence', 'numero', 'monto', 'monto_pagado', 'fecha_pago',
                  'medio_pago', 'referencia_pago')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            if instance.poliza:
                kwargs.update(
                    initial={
                        'nombre_cliente': instance.cliente_poliza['name'],
                        'numero_poliza': instance.poliza.no_poliza,
                        'aseguradora': instance.poliza.aseguradora.name,
                        'numero_recibo': instance.poliza.no_recibo,
                    }
                )
            if instance.tramite:
                kwargs.update(
                    initial={
                        'nombre_cliente': instance.cliente_tramite['name'],
                        'numero_poliza': instance.tramite.poliza.no_poliza,
                        'aseguradora': instance.tramite.poliza.aseguradora.name,
                        'numero_recibo': instance.tramite.no_recibo,
                    }
                )
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['monto_pagado'].widget.attrs['min'] = 0.0
            self.fields['monto_pagado'].widget.attrs['max'] = instance.monto

    def clean(self):
        data = self.cleaned_data
        if data['monto_pagado'] > data['monto']:
            raise forms.ValidationError("el monto pagado no puede ser mayor al monto a pagar", )

    def save(self, commit=True):
        super().save(commit)
        data = self.cleaned_data
        instance = self.instance
        if instance and data['monto'] == data['monto_pagado']:
            instance.estado = EstadoPago.PAGADO
            instance.save()


class ComisionForm(forms.ModelForm):
    nombre_cliente = forms.CharField(label="Nombre del cliente", required=False,
                                     widget=forms.TextInput(
                                         attrs={
                                             'readonly': 'readonly'
                                         }
                                     ))
    numero_poliza = forms.CharField(label="Número de póliza", required=False,
                                    widget=forms.TextInput(
                                        attrs={
                                            'readonly': 'readonly'
                                        }
                                    ))
    aseguradora = forms.CharField(label="Aseguradora", required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'readonly': 'readonly'
                                      }
                                  ))
    numero_recibo = forms.CharField(label="Número de recibo", required=False,
                                    widget=forms.TextInput(
                                        attrs={
                                            'readonly': 'readonly'
                                        }
                                    ))
    fecha_vence = forms.CharField(label="Fecha de vencimiento", required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'readonly': 'readonly'
                                      }
                                  ))
    numero = forms.IntegerField(label="Número de cuota", required=False,
                                widget=forms.NumberInput(
                                    attrs={
                                        'readonly': 'readonly'
                                    }
                                ))
    monto = forms.FloatField(label="Valor a pagar", required=False,
                             widget=forms.NumberInput(
                                 attrs={
                                     'readonly': 'readonly'
                                 }
                             ))
    monto_pagado = forms.FloatField(label="Monto pagado", required=False,
                                    widget=forms.NumberInput(
                                        attrs={
                                            'readonly': 'readonly'
                                        }
                                    ))
    fecha_pago = forms.CharField(label="Fecha de pago", required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         'readonly': 'readonly'
                                     }
                                 ))
    medio_pago = forms.ChoiceField(choices=MedioPago.choices(), label="Medio de pago",
                                   widget=forms.Select(
                                       attrs={
                                           'readonly': 'readonly'
                                       }
                                   ))
    referencia_pago = forms.CharField(label="Referencia de pago", required=False,
                                      widget=forms.TextInput(
                                          attrs={
                                              'readonly': 'readonly'
                                          }
                                      ))

    class Meta:
        model = Pago
        fields = ('nombre_cliente', 'numero_poliza', 'aseguradora', 'numero_recibo',
                  'fecha_vence', 'numero', 'monto', 'monto_pagado', 'fecha_pago',
                  'medio_pago', 'monto_comision', 'fecha_pago_comision', 'referencia_pago')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            if instance.poliza:
                kwargs.update(
                    initial={
                        'nombre_cliente': instance.cliente_poliza['name'],
                        'numero_poliza': instance.poliza.no_poliza,
                        'aseguradora': instance.poliza.aseguradora.name,
                        'numero_recibo': instance.poliza.no_recibo,
                    }
                )
            if instance.tramite:
                kwargs.update(
                    initial={
                        'nombre_cliente': instance.cliente_tramite['name'],
                        'numero_poliza': instance.tramite.poliza.no_poliza,
                        'aseguradora': instance.tramite.poliza.aseguradora.name,
                        'numero_recibo': instance.tramite.no_recibo,
                    }
                )
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['monto_pagado'].widget.attrs['min'] = 0.0
            self.fields['monto_pagado'].widget.attrs['max'] = instance.monto

    def clean(self):
        data = self.cleaned_data
        if data['monto_pagado'] > data['monto']:
            raise forms.ValidationError("el monto pagado no puede ser mayor al monto a pagar", )

    def save(self, commit=True):
        super().save(commit)
        data = self.cleaned_data
        instance = self.instance
        if instance and data['monto'] == data['monto_pagado']:
            instance.estado = EstadoPago.PAGADO
            instance.save()


class ReciboForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
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

    prima_total = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ), initial=0.0)
    saldo_pendiente = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ), initial=0.0)

    recibos = forms.Field(required=False, label="Recibos de esta póliza",
                          widget=RecibosPrima)

    class Meta:
        model = Poliza
        fields = (
            'no_poliza', 'ramo', 'sub_ramo', 'fecha_emision', 'fecha_vence', 'aseguradora',
            'cliente', 'grupo', 'tipo_poliza', 'cesion_derecho',
            'estado_poliza', 'no_recibo', 'concepto', 'pedir_comentarios',
            'f_pago', 'm_pago', 'cuotas', 'fecha_pago', 'subtotal', 'descuento',
            'emision', 'iva', 'otros', 'total', 'per_comision', 'suma_asegurada',
            'amount_comision', 'moneda', 'tabla_pagos', 'recibos'
        )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            updated_initial['campos_adicionales'] = instance
            try:
                updated_initial['fecha_vence'] = instance.fecha_vence.strftime('%d/%m/%Y')
            except AttributeError:
                pass
            updated_initial['recibos'] = instance
            updated_initial['tabla_pagos'] = instance
            updated_initial['pedir_comentarios'] = instance.perdir_comentarios
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)
        if instance and not instance.editable:
            self.fields['no_poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['no_recibo'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_vence'].widget.attrs['readonly'] = 'readonly'
            self.fields['ramo'].widget.attrs['readonly'] = 'readonly'
            self.fields['sub_ramo'].widget.attrs['readonly'] = 'readonly'
            self.fields['aseguradora'].widget.attrs['readonly'] = 'readonly'
            self.fields['cliente'].widget.attrs['disabled'] = 'disabled'
            self.fields['grupo'].widget.attrs['readonly'] = 'readonly'
            self.fields['tipo_poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['cesion_derecho'].widget.attrs['readonly'] = 'readonly'
            self.fields['concepto'].widget.attrs['readonly'] = 'readonly'
        if instance:
            if instance.f_pago == FormaPago.CONTADO:
                self.fields['cuotas'].widget.attrs['readonly'] = 'readonly'
        if instance and (instance.estado_poliza == EstadoPoliza.CANCELADA
                         or instance.estado_poliza == EstadoPoliza.ANULADA):
            self.fields['tipo_poliza'].required = False
            self.fields['cliente'].required = False
        if instance and not instance.estado_poliza == EstadoPoliza.PENDIENTE:
            self.fields['moneda'].widget.attrs['readonly'] = 'readonly'
            self.fields['f_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['m_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['cuotas'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
            self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
            self.fields['emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['iva'].widget.attrs['readonly'] = 'readonly'
            self.fields['otros'].widget.attrs['readonly'] = 'readonly'
            self.fields['total'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'
