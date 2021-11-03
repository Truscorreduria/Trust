from django import forms
from .widgets import *
from backend.models import *
import calendar
from django.contrib.humanize.templatetags.humanize import intcomma


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


class ArchivoClienteForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('tipo_doc',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['tipo_doc'].widget.attrs['data-id'] = instance.id


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
                ('total', 'Prima neta'),
                ('estado', 'Estado'),
                ('ver', ''),
            )
        }
    ))
    polizas_renovadas = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('no_poliza', 'Número de póliza'),
                ('aseguradora', 'Aseguradora'),
                ('ramo', 'Ramo'),
                ('fecha_emision', 'Fecha inicio'),
                ('fecha_vence', 'Fecha fin'),
                ('dias_vigencia', 'Vence'),
                ('grupo', 'Grupo'),
                ('total', 'Prima neta'),
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

    documentos = forms.Field(widget=DriveClienteWidget(
        attrs={
            'form': ArchivoClienteForm
        }
    ), required=False, label="")

    class Meta:
        model = ClienteJuridico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        request = kwargs.pop('request', None)
        updated_initial = {}
        if instance:
            updated_initial['contactos'] = instance.contactos()
            updated_initial['polizas'] = instance.polizas_activas_section().order_by('no_poliza')
            updated_initial['polizas_renovadas'] = instance.polizas_renovadas_section().order_by('no_poliza')
            updated_initial['tramites'] = instance.tramites()
            updated_initial['documentos'] = instance.media_files
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
                ('total', 'Prima neta'),
                ('estado', 'Estado'),
                ('ver', ''),
            )
        }
    ))
    polizas_renovadas = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('no_poliza', 'Número de póliza'),
                ('aseguradora', 'Aseguradora'),
                ('ramo', 'Ramo'),
                ('fecha_emision', 'Fecha inicio'),
                ('fecha_vence', 'Fecha fin'),
                ('dias_vigencia', 'Vence'),
                ('grupo', 'Grupo'),
                ('total', 'Prima neta'),
                ('estado', 'Estado'),
                ('ver', ''),
            )
        }
    ))

    documentos = forms.Field(widget=DriveClienteWidget(
        attrs={
            'form': ArchivoClienteForm
        }
    ), required=False, label="")

    class Meta:
        model = ClienteNatural
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        request = kwargs.pop('request', None)
        updated_initial = {}
        if instance:
            updated_initial['polizas'] = instance.polizas_activas_section().order_by('no_poliza')
            updated_initial['polizas_renovadas'] = instance.polizas_renovadas_section().order_by('no_poliza')
            updated_initial['tramites'] = instance.tramites()
            updated_initial['documentos'] = instance.media_files
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
        fields = ('order', 'name', 'label',)


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


class LineaForm(forms.ModelForm):
    aseguradoras = forms.ModelMultipleChoiceField(queryset=Aseguradora.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  label="Aseguradoras con las que cotiza.",
                                                  required=False)

    class Meta:
        model = Linea
        fields = '__all__'


class PolizaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
    contratante = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Contratante',
                                         required=True, widget=SelectSearch)
    cesioinario = forms.ModelChoiceField(queryset=ClienteJuridico.objects.filter(es_cesionario=True),
                                         required=False, label="Cesionario")
    coberturas = forms.Field(label="", required=False, widget=CoberturasWidget)
    tabla_pagos = forms.Field(label="", required=False, widget=TablaPagosWidget)
    campos_adicionales = forms.Field(label="", required=False, widget=CamposAdicionalesWidget)
    tramites = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('code', 'Número de trámite'),
                ('tipo_tramite_display', 'Tipo trámite'),
                ('user', 'Ingresado por'),
                ('no_recibo', 'Número de recibo'),
                ('created', 'Fecha de registro'),
                ('estado', 'Estado'),
                ('ver', 'Ver'),
            )
        }
    ))
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

    prima_total = forms.CharField(required=False, label="", initial=0.0)
    saldo_pendiente = forms.CharField(required=False, label="", initial=0.0)

    otro_motivo = forms.CharField(required=False, label="Especificar motivo",
                                  widget=forms.Textarea(attrs={
                                      'rows': 4,
                                  }))

    ejecutivo = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    oportunidad = forms.CharField(max_length=8, label='Oportunidad de negocio', required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'readonly': 'readonly'
                                      }
                                  ))

    class Meta:
        model = Poliza
        fields = (
            'no_poliza', 'ramo', 'sub_ramo', 'fecha_emision', 'fecha_vence', 'aseguradora',
            'cliente', 'contratante', 'grupo', 'tipo_poliza', 'cesion_derecho', 'cesioinario',
            'estado_poliza', 'no_recibo', 'concepto', 'pedir_comentarios', 'coberturas',
            'fecha_cancelacion', 'motivo_cancelacion', 'otro_motivo',
            'f_pago', 'm_pago', 'cantidad_cuotas', 'fecha_pago', 'subtotal', 'descuento',
            'emision', 'iva', 'otros', 'total', 'per_comision', 'suma_asegurada',
            'amount_comision', 'moneda', 'tabla_pagos', 'campos_adicionales', 'drive', 'bitacora',
            'per_comision_eje', 'amount_comision_eje', 'comisionista', 'ejecutivo', 'oportunidad',
            'user_create',
        )
        localized_fields = ('subtotal', 'descuento', 'emision', 'iva', 'otros', 'suma_asegurada',
                            'amount_comision', 'prima_neta', 'total', 'prima_total', 'saldo_pendiente')

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
            updated_initial['tramites'] = instance.tramites()
            updated_initial['drive'] = instance
            updated_initial['bitacora'] = instance
            updated_initial['pedir_comentarios'] = instance.perdir_comentarios
            updated_initial['prima_total'] = intcomma(instance.prima_total())
            updated_initial['saldo_pendiente'] = intcomma(instance.saldo_pendiente())
            if instance.oportunity:
                updated_initial['oportunidad'] = instance.oportunity.code
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)
        self.fields['total'].widget.attrs['readonly'] = 'readonly'
        self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'
        self.fields['prima_total'].widget.attrs['readonly'] = 'readonly'
        self.fields['saldo_pendiente'].widget.attrs['readonly'] = 'readonly'
        if instance and not instance.editable:
            self.fields['no_poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['no_recibo'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_emision'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_vence'].widget.attrs['readonly'] = 'readonly'
            self.fields['ramo'].widget.attrs['readonly'] = 'readonly'
            self.fields['sub_ramo'].widget.attrs['readonly'] = 'readonly'
            self.fields['aseguradora'].widget.attrs['readonly'] = 'readonly'
            self.fields['ejecutivo'].widget.attrs['readonly'] = 'readonly'
            self.fields['cliente'].widget.attrs['disabled'] = 'disabled'
            self.fields['contratante'].widget.attrs['disabled'] = 'disabled'
            self.fields['grupo'].widget.attrs['readonly'] = 'readonly'
            self.fields['tipo_poliza'].widget.attrs['readonly'] = 'readonly'
            self.fields['cesion_derecho'].widget.attrs['readonly'] = 'readonly'
            self.fields['cesioinario'].widget.attrs['readonly'] = 'readonly'
            self.fields['concepto'].widget.attrs['readonly'] = 'readonly'
            self.fields['comisionista'].widget.attrs['readonly'] = 'readonly'
            self.fields['per_comision_eje'].widget.attrs['readonly'] = 'readonly'
            self.fields['amount_comision_eje'].widget.attrs['readonly'] = 'readonly'
        if instance:
            if instance.f_pago == FormaPago.CONTADO:
                self.fields['cantidad_cuotas'].widget.attrs['readonly'] = 'readonly'
        if instance and (instance.estado_poliza == EstadoPoliza.CANCELADA
                         or instance.estado_poliza == EstadoPoliza.ANULADA):
            self.fields['tipo_poliza'].required = False
            self.fields['cliente'].required = False
            self.fields['contratante'].required = False
        if instance and not instance.estado_poliza == EstadoPoliza.PENDIENTE:
            self.fields['moneda'].widget.attrs['readonly'] = 'readonly'
            self.fields['f_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['m_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['cantidad_cuotas'].widget.attrs['readonly'] = 'readonly'
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
    prima_neta = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly',
        }
    ))
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(), required=False,
                                    widget=forms.Select(
                                        choices=[]
                                    ))

    class Meta:
        model = Tramite
        exclude = ('editable',)
        localized_fields = ('subtotal', 'descuento', 'emision', 'iva', 'otros', 'suma_asegurada',
                            'amount_comision', 'prima_neta', 'total', 'amount_comision')

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
            updated_initial['prima_neta'] = intcomma(instance.prima_neta())
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
        self.fields['total'].widget.attrs['readonly'] = 'readonly'
        self.fields['amount_comision'].widget.attrs['readonly'] = 'readonly'
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
            self.fields['cantidad_cuotas'].widget.attrs['readonly'] = 'readonly'
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
            self.fields['cliente'].widget.attrs['readonly'] = 'readonly'

    def clean_no_recibo(self):
        value = self.cleaned_data.get('no_recibo')
        if self.instance and value:
            if self.instance.id:
                related = list(
                    Tramite.objects.filter(poliza=self.instance.poliza).exclude(id=self.instance.id).values_list(
                        'no_recibo', flat=True))
                related.append(self.instance.poliza.no_recibo)
                if value in related:
                    raise forms.ValidationError('Recibo de prima duplicado, por favor revise')
        return value


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

    email_texto = forms.CharField(required=True, label="Contenido del correo (Accede a datos de "
                                                       "la poliza de la siguiente manera: [[ poliza.cliente ]])",
                                  widget=forms.Textarea(
                                      attrs={
                                          'class': "htmleditor",
                                          'data-autosave': "editor-content",
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
    cedula = forms.CharField(required=False, label="Número indentificación")
    ruc = forms.CharField(required=False, label="Número indentificación")
    domicilio = forms.CharField(label="Dirección", required=False, widget=forms.Textarea(
        attrs={
            'rows': '4',
        }
    ))
    observaciones = forms.CharField(label="Observaciones", required=False, widget=forms.Textarea(
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
            self.fields['actividad_economica'].widget.attrs['readonly'] = 'readonly'
            self.fields['razon_social'].widget.attrs['readonly'] = 'readonly'
            self.fields['nombre_comercial'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_constitucion'].widget.attrs['readonly'] = 'readonly'
            self.fields['pagina_web'].widget.attrs['readonly'] = 'readonly'
            self.fields['observaciones'].widget.attrs['readonly'] = 'readonly'
        else:
            self.fields['cedula'].widget.attrs['readonly'] = 'readonly'
            self.fields['tipo_cliente'].widget.attrs['readonly'] = 'readonly'
            self.fields['tipo_identificacion'].widget.attrs['readonly'] = 'readonly'


class OportunityForm(forms.ModelForm):
    status = forms.Field(widget=OportunityStatusWidget, label="", initial=OportunityStatus.PENDIENTE)
    days = forms.CharField(label="Dias transcurridos", required=False, widget=forms.TextInput(
        attrs={
            'readonly': 'readonly'
        }
    ))
    prospect = forms.ModelChoiceField(queryset=Prospect.objects.all(), label="Prospecto", required=False,
                                      widget=ProspectFormWidget(
                                          attrs={
                                              'form': ProspectForm
                                          }
                                      ))
    drive = forms.Field(label="", required=False, widget=DriveWidget)
    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)

    extra_data = forms.Field(label="", required=False, widget=JsonWidget)

    cotizacion = forms.Field(label="", required=False, widget=CotizacionWidget(
        attrs={
            'companies': [],
            'instance': None,
        }
    ))
    code = forms.CharField(widget=forms.HiddenInput, required=False)
    vendedor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True).order_by('first_name'))
    campain = forms.ModelChoiceField(queryset=Campain.objects.all())

    class Meta:
        model = Oportunity
        exclude = ('linea',)
        localized_fields = ('valor_nuevo', 'valor_exceso')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        try:
            linea = kwargs.pop('linea')
        except:
            linea = None
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
            self.fields['cotizacion'].widget.attrs['companies'] = instance.linea.aseguradoras.all().order_by('code')
        if linea:
            self.fields['campain'].queryset = Campain.objects.filter(active=True, linea=linea)
            self.fields['cotizacion'].widget.attrs['companies'] = linea.aseguradoras.all().order_by('code')


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


class ReciboForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
    tabla_pagos = forms.Field(label="", required=False, widget=CobranzaWidget)
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

    prima_neta = forms.FloatField(required=False, label="", widget=forms.NumberInput(
        attrs={
            'readonly': 'readonly',
        }
    ))
    saldo_pendiente = forms.FloatField(required=False, label="", widget=forms.NumberInput(
        attrs={
            'readonly': 'readonly'
        }
    ), initial=0.0)

    recibos = forms.Field(required=False, label="Recibos de esta póliza",
                          widget=RecibosPrima)
    no_tramite = forms.CharField(required=False, label="Número de trámite",
                                 widget=forms.TextInput(attrs={
                                     'readonly': 'readonly'
                                 }))
    prima_total = forms.FloatField(required=False, label="Prima total",
                                   widget=forms.NumberInput(
                                       attrs={
                                           'readonly': 'readonly'
                                       }
                                   ))

    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)

    class Meta:
        model = Poliza
        fields = (
            'no_poliza', 'ramo', 'sub_ramo', 'fecha_emision', 'fecha_vence', 'aseguradora',
            'cliente', 'grupo',
            'f_pago', 'm_pago', 'cantidad_cuotas', 'fecha_pago', 'subtotal', 'descuento',
            'emision', 'iva', 'otros', 'total', 'per_comision', 'suma_asegurada',
            'amount_comision', 'moneda', 'tabla_pagos', 'recibo_editar', 'recibos'
        )
        localized_fields = ('subtotal', 'descuento', 'emision', 'iva', 'otros', 'suma_asegurada',
                            'amount_comision', 'prima_neta', 'total', 'amount_comision')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        updated_initial = {}
        if instance:
            try:
                updated_initial['fecha_vence'] = instance.fecha_vence.strftime('%d/%m/%Y')
            except AttributeError:
                pass
            updated_initial['recibos'] = instance
            updated_initial['prima_total'] = instance.prima_total
            updated_initial['saldo_pendiente'] = instance.saldo_pendiente
            updated_initial['bitacora'] = instance
            if instance.recibo_editar:
                updated_initial['tabla_pagos'] = instance.recibo_editar
                updated_initial['subtotal'] = instance.recibo_editar.subtotal
                updated_initial['descuento'] = instance.recibo_editar.descuento
                updated_initial['emision'] = instance.recibo_editar.emision
                updated_initial['iva'] = instance.recibo_editar.iva
                updated_initial['otros'] = instance.recibo_editar.otros
                updated_initial['total'] = instance.recibo_editar.total
                updated_initial['prima_neta'] = instance.recibo_editar.prima_neta
                updated_initial['per_comision'] = instance.recibo_editar.per_comision
                updated_initial['suma_asegurada'] = instance.recibo_editar.suma_asegurada
                updated_initial['amount_comision'] = instance.recibo_editar.amount_comision
                updated_initial['moneda'] = instance.recibo_editar.moneda
                updated_initial['f_pago'] = instance.recibo_editar.f_pago
                updated_initial['m_pago'] = instance.recibo_editar.m_pago
                updated_initial['cantidad_cuotas'] = instance.recibo_editar.cantidad_cuotas
                updated_initial['fecha_pago'] = instance.recibo_editar.fecha_pago
                updated_initial['no_tramite'] = instance.recibo_editar.code
            else:
                updated_initial['tabla_pagos'] = instance
                updated_initial['prima_neta'] = instance.prima_neta
        kwargs.update(initial=updated_initial)
        super().__init__(*args, **kwargs)
        self.fields['no_poliza'].widget.attrs['readonly'] = 'readonly'
        self.fields['fecha_emision'].widget.attrs['readonly'] = 'readonly'
        self.fields['fecha_vence'].widget.attrs['readonly'] = 'readonly'
        self.fields['ramo'].widget.attrs['readonly'] = 'readonly'
        self.fields['sub_ramo'].widget.attrs['readonly'] = 'readonly'
        self.fields['aseguradora'].widget.attrs['readonly'] = 'readonly'
        self.fields['cliente'].widget.attrs['readonly'] = 'readonly'
        self.fields['grupo'].widget.attrs['readonly'] = 'readonly'
        if instance:
            if not instance.modificando_recibo:
                self.fields['f_pago'].widget.attrs['readonly'] = 'readonly'
                self.fields['m_pago'].widget.attrs['readonly'] = 'readonly'
                self.fields['cantidad_cuotas'].widget.attrs['readonly'] = 'readonly'
                self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
                self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
                self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
                self.fields['emision'].widget.attrs['readonly'] = 'readonly'
                self.fields['iva'].widget.attrs['readonly'] = 'readonly'
                self.fields['otros'].widget.attrs['readonly'] = 'readonly'
                self.fields['total'].widget.attrs['readonly'] = 'readonly'
                self.fields['per_comision'].widget.attrs['readonly'] = 'readonly'
                self.fields['suma_asegurada'].widget.attrs['readonly'] = 'readonly'
                self.fields['moneda'].widget.attrs['readonly'] = 'readonly'
                self.fields['tabla_pagos'].widget.attrs['readonly'] = 'readonly'
            else:
                self.fields['recibos'].widget.attrs['readonly'] = 'readonly'
                if instance.con_pagos():
                    self.fields['f_pago'].widget.attrs['readonly'] = 'readonly'
                    self.fields['m_pago'].widget.attrs['readonly'] = 'readonly'
                    self.fields['cantidad_cuotas'].widget.attrs['readonly'] = 'readonly'
                    self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
                    self.fields['subtotal'].widget.attrs['readonly'] = 'readonly'
                    self.fields['descuento'].widget.attrs['readonly'] = 'readonly'
                    self.fields['emision'].widget.attrs['readonly'] = 'readonly'
                    self.fields['iva'].widget.attrs['readonly'] = 'readonly'
                    self.fields['otros'].widget.attrs['readonly'] = 'readonly'
                    self.fields['moneda'].widget.attrs['readonly'] = 'readonly'


class PagoForm(forms.ModelForm):
    prefix = 'pagocuota'

    class Meta:
        model = PagoCuota
        fields = ('monto', 'referencia_pago', 'medio_pago', 'fecha_pago', 'comision', 'fecha_pago_comision')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance and instance.cuota.estado == EstadoPago.PAGADO:
            self.fields['fecha_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['monto'].widget.attrs['readonly'] = 'readonly'
            self.fields['referencia_pago'].widget.attrs['readonly'] = 'readonly'
            self.fields['medio_pago'].widget.attrs['readonly'] = 'readonly'


class CuotaForm(forms.ModelForm):
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
    # numero = forms.IntegerField(label="Número de cuota", required=False,
    #                             widget=forms.NumberInput(
    #                                 attrs={
    #                                     'readonly': 'readonly'
    #                                 }
    #                             ))
    monto = forms.FloatField(label="Valor a pagar", required=False,
                             widget=forms.NumberInput(
                                 attrs={
                                     'readonly': 'readonly'
                                 }
                             ))
    saldo = forms.FloatField(label="Saldo", required=False,
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
    monto_comision = forms.FloatField(label="Monto comisión", required=False,
                                      widget=forms.NumberInput(
                                          attrs={
                                              'readonly': 'readonly'
                                          }
                                      ))
    comision_pagada = forms.FloatField(label="Comision recibida", required=False,
                                       widget=forms.NumberInput(
                                           attrs={
                                               'readonly': 'readonly'
                                           }
                                       ))
    comision_pendiente = forms.FloatField(label="Comision pendiente", required=False,
                                          widget=forms.NumberInput(
                                              attrs={
                                                  'readonly': 'readonly'
                                              }
                                          ))
    dias_mora = forms.IntegerField(label="Días de mora", required=False,
                                   widget=forms.NumberInput(
                                       attrs={
                                           'readonly': 'readonly'
                                       }
                                   )
                                   )
    pagos = forms.Field(label="Pagos realizados", required=False, widget=PagosWidget(
        attrs={
            'form': PagoForm
        }
    ))

    moneda = forms.ModelChoiceField(label="Moneda", queryset=Moneda.objects.all(), required=False,
                                    widget=forms.Select(
                                        attrs={
                                            'readonly': 'readonly',
                                        }
                                    ))

    class Meta:
        model = Cuota
        fields = ('nombre_cliente', 'numero_poliza', 'aseguradora', 'numero_recibo',
                  'fecha_vence', 'monto', 'dias_mora', 'monto_comision', 'estado',
                  'monto_pagado', 'comision_pagada', 'saldo', 'comision_pendiente', 'moneda')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            update_initial = {}
            if instance.poliza:
                update_initial = {
                    'nombre_cliente': instance.cliente_poliza['name'],
                    'numero_poliza': instance.poliza.no_poliza,
                    'aseguradora': instance.poliza.aseguradora.name,
                    'numero_recibo': instance.poliza.no_recibo,
                    'moneda': instance.poliza.moneda,
                }
            if instance.tramite:
                update_initial = {
                    'nombre_cliente': instance.cliente_tramite['name'],
                    'numero_poliza': instance.tramite.poliza.no_poliza,
                    'aseguradora': instance.tramite.poliza.aseguradora.name,
                    'numero_recibo': instance.tramite.no_recibo,
                    'moneda': instance.tramite.moneda,
                }
            update_initial['pagos'] = instance.pagos
            update_initial['dias_mora'] = instance.dias_mora
            update_initial['monto_pagado'] = instance.monto_pagado
            update_initial['saldo'] = instance.saldo
            update_initial['comision_pagada'] = instance.comision_pagada
            update_initial['comision_pendiente'] = instance.comision_pendiente
            kwargs.update(initial=update_initial)
        super().__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs['readonly'] = 'readonly'
        if instance:
            self.fields['pagos'].widget.attrs['cuota'] = instance

    def save(self, commit=True):
        super().save(commit)
        data = self.cleaned_data
        instance = self.instance
        if instance and data['monto'] == instance.monto_pagado():
            instance.estado = EstadoPago.PAGADO
            instance.save()


class SiniestroTramiteForm(forms.ModelForm):
    code = forms.CharField(required=False, label="Tramite Interno", widget=forms.TextInput(
        attrs={
            'readonly': 'readonly',
        }
    ))

    ramo = forms.CharField(required=False, label="Ramo", widget=ReadOnlyWidget)
    sub_ramo = forms.CharField(required=False, label="Sub ramo", widget=ReadOnlyWidget)
    grupo = forms.CharField(required=False, label="Grupo", widget=ReadOnlyWidget)
    aseguradora = forms.CharField(required=False, label="Aseguradora", widget=ReadOnlyWidget)
    descripcion = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'rows': 4
        }
    ))
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
    drive = forms.Field(label="", required=False, widget=DriveWidget)
    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)

    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(), required=False,
                                    widget=forms.Select(
                                        choices=[]
                                    ))

    class Meta:
        model = SiniestroTramite
        fields = '__all__'

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
            updated_initial['drive'] = instance
            updated_initial['bitacora'] = instance
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
        if instance and (instance.estado == 'Pagado' or instance.estado == 'Rechazado'):
            self.fields['estado'].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        data = self.cleaned_data
        return data


class SiniestroForm(forms.ModelForm):
    reclamo_aseguradora = forms.CharField(max_length=50, required=True, label="Número de Reclamo")
    ramo = forms.CharField(required=False, label="Ramo", widget=ReadOnlyWidget)
    sub_ramo = forms.CharField(required=False, label="Sub ramo", widget=ReadOnlyWidget)
    grupo = forms.CharField(required=False, label="Grupo", widget=ReadOnlyWidget)

    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente',
                                     required=True, widget=SelectSearch)
    drive = forms.Field(label="", required=False, widget=DriveWidget)
    bitacora = forms.Field(label="", required=False, widget=BitacoraWidget)

    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(), required=False,
                                    widget=forms.Select(
                                        choices=[]
                                    ))

    class Meta:
        model = Siniestro
        fields = '__all__'

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
            updated_initial['drive'] = instance
            updated_initial['bitacora'] = instance
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
        self.fields['poliza'].choices = []
        if instance and instance.cliente:
            self.fields['poliza'].choices = self.get_poliza_choices(instance.cliente)

        if instance and (instance.estado == 'Pagado' or instance.estado == 'Rechazado'):
            self.fields['estado'].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        data = self.cleaned_data
        return data


class BasePolizaFilterForm(forms.Form):
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
    ramo = forms.ModelChoiceField(queryset=SubRamo.objects.all(), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), required=False,
                                  label="Usuario")


class ReportPolizaForm(BasePolizaFilterForm):
    fecha_emision__gte = forms.DateField(required=True, label="Desde")
    fecha_emision__lte = forms.DateField(required=True, label="Hasta")


class ReportPolizaVencerForm(BasePolizaFilterForm):
    fecha_vence__gte = forms.DateField(required=True, label="Desde")
    fecha_vence__lte = forms.DateField(required=True, label="Hasta")


class ReportTramiteForm(forms.Form):
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False,
                                     widget=SelectSearch)
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.all(), required=False,
                                    widget=SelectSearch)
    estado = forms.ChoiceField(choices=EstadoTramite.choices(), required=False)
    created__gte = forms.DateField(required=True, label="Desde")
    created__lte = forms.DateField(required=True, label="Hasta")


class ReporteCrmForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=Linea.objects.all(), required=True)
    campain = forms.ModelChoiceField(queryset=Campain.objects.all(), required=False, label="Campaña")
    vendedor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), required=False)
    status = forms.ChoiceField(choices=(('', '---------'),) + OportunityStatus.choices(),
                               required=False, label="Estado")
    # created__gte = forms.DateField(required=True, label="Desde")
    # created__lte = forms.DateField(required=True, label="Hasta")


class ReporteSiniestroForm(forms.Form):
    estado = forms.ChoiceField(choices=EstadoSiniestro.choices(), required=False)
    ramo = forms.ModelChoiceField(queryset=Ramo.objects.all(), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False,
                                     widget=SelectSearch)
    poliza = forms.ModelChoiceField(queryset=Poliza.objects.filter(estado_poliza=EstadoPoliza.ACTIVA), required=False,
                                    widget=SelectSearch)
    created__gte = forms.DateField(required=True, label="Desde")
    created__lte = forms.DateField(required=True, label="Hasta")


class ReporteCarteraForm(forms.Form):
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
    ramo = forms.ModelChoiceField(queryset=Ramo.objects.all(), required=False)
    moneda = forms.ModelChoiceField(queryset=Moneda.objects.all(), required=False, label="Moneda")
    aseguradora = forms.ModelChoiceField(queryset=Aseguradora.objects.all(), required=False, label="Compañia")
    date = forms.DateField(required=True, label="Fecha de corte")


class ReporteComisionForm(forms.Form):
    poliza__ramo = forms.ModelChoiceField(queryset=Ramo.objects.all(), required=False)
    poliza__grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
    poliza__moneda = forms.ModelChoiceField(queryset=Moneda.objects.all(), required=False)
    fecha_pago__gte = forms.DateField(required=True, label="Desde")
    fecha_pago__lte = forms.DateField(required=True, label="Hasta")


class DashboardFiltersForm(forms.Form):
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False, empty_label='TODOS')
    desde = forms.DateField(required=True, label="Desde", widget=forms.DateInput(
        attrs={
            'class': 'form-control-sm'
        }
    ))
    hasta = forms.DateField(required=True, label="Hasta", widget=forms.DateInput(
        attrs={
            'class': 'form-control-sm'
        }
    ))

    def __init__(self, *args, **kwargs):
        now = timezone.now()
        desde = timezone.datetime(year=now.year, month=now.month, day=1)
        _, days = calendar.monthrange(desde.year, desde.month)
        hasta = desde + timedelta(days=days - 1)
        kwargs.update(initial={
            'desde': desde, 'hasta': hasta
        })
        super().__init__(*args, **kwargs)


class GrupoForm(forms.ModelForm):
    email_cliente = forms.CharField(label="", required=False,
                                    widget=forms.Textarea(attrs={
                                        'class': "htmleditor",
                                        'data-autosave': "editor-content",
                                    }))

    class Meta:
        model = Grupo
        fields = '__all__'


class EmailForm(forms.Form):
    de = forms.CharField(max_length=250, required=True, label="de")
    para = forms.CharField(max_length=250, required=True, label="Para")
    asunto = forms.CharField(max_length=250, required=True, label="Asunto")
    contenido = forms.CharField(max_length=10000, required=True, label="",
                                widget=forms.Textarea(
                                    attrs={
                                        'class': 'htmleditor'
                                    }
                                ))


class PassengersTravelForm(forms.ModelForm):
    prefix = "passengers"

    class Meta:
        model = PassengersTravel
        exclude = ('asistencia', 'documento')


class AsistenciaTravelForm(forms.ModelForm):
    passengers = forms.Field(label="Datos de los viajeros", required=False,
                             widget=TableBorderedInput(
                                 attrs={
                                     'form': PassengersTravelForm
                                 }
                             ))

    class Meta:
        model = AsistenciaTravel
        # fields = '__all__'
        exclude = ('pais_destino',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(initial={
                'passengers': instance.passengers.all()
            })
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['readonly'] = 'readonly'
        self.fields['valor'].widget.attrs['readonly'] = 'readonly'
        self.fields['documento'].widget.attrs['readonly'] = 'readonly'
        self.fields['referencia'].widget.attrs['readonly'] = 'readonly'
        self.fields['ruta'].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = self.cleaned_data
