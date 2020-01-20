from django.db import models
from grappelli_extras.models import base, BaseEntity, get_code
from django.contrib.auth.models import User
from utils.models import Departamento, Municipio
from django.contrib.contenttypes.models import ContentType
from simple_history.models import HistoricalRecords


def try_json(instanse, model):
    try:
        return instanse.to_json()
    except:
        return model().to_json()


class Ramo(base):
    nombre = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.nombre


class SubRamo(base):
    ramo = models.ForeignKey(Ramo, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250, null=True)

    def __str__(self):
        text = []
        if self.ramo:
            text.append(self.ramo.nombre)
        text.append(self.nombre)
        return " - ".join(text)


class Aseguradora(base):
    nombre = models.CharField(max_length=200, null=True)
    ruc = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=8, null=True)
    departamento = models.ForeignKey(Departamento, null=True, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, null=True, on_delete=models.CASCADE)
    direccion = models.TextField(max_length=250, null=True)
    cuenta_bancaria = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def to_json(self):
        o = super().to_json()
        o['departamento'] = try_json(self.departamento, Departamento)
        o['municipio'] = try_json(self.municipio, Municipio)
        return o


class aseguradoraSubRamo(base):
    aseguradora = models.ForeignKey(Aseguradora, null=True, on_delete=models.CASCADE)
    sub_ramo = models.ForeignKey(SubRamo, null=True, on_delete=models.CASCADE)
    comision = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)

    def __str__(self):
        return "%s - %s" % (self.aseguradora.nombre, self.sub_ramo.nombre)


# region cliente


TIPOS_IDENTIFICACION = (
    (1, 'Cédula nicaraguense'),
    (2, 'Cédula de residencia'),
    (3, 'Pasaporte'),
    (4, 'RUC'),
)


class baseCliente(base):
    tipo_identificacion = models.PositiveSmallIntegerField(choices=TIPOS_IDENTIFICACION, default=1)
    numero_identificacion = models.CharField(max_length=45, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, null=True, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=8, null=True, blank=True)
    celular = models.CharField(max_length=8, null=True, blank=True)
    email_principal = models.EmailField(max_length=200, null=True, blank=True)
    email_alterno = models.EmailField(max_length=200, null=True, blank=True)
    correo_poliza_vencer = models.BooleanField(default=False)
    correo_cartera_vencer = models.BooleanField(default=False)
    sms_poliza_vencer = models.BooleanField(default=False)
    sms_cartera_vencer = models.BooleanField(default=False)
    link_accesso = models.CharField(max_length=250, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True)

    class Meta:
        abstract = True


class Persona(base):
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    primer_nombre = models.CharField(max_length=45, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=45, null=True, blank=True)
    primer_apellido = models.CharField(max_length=45, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=45, null=True, blank=True)
    genero = models.CharField(max_length=1, null=True, blank=True, choices=GENEROS)
    # vencimiento_documento = models.DateField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estado_civil = models.CharField(max_length=20, null=True, blank=True)
    ocupacion = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        abstract = True


class Empresa(base):
    razon_social = models.CharField(max_length=250, null=True, blank=True)
    fecha_expedicion = models.DateField(null=True, blank=True)
    fecha_constitucion = models.DateField(null=True, blank=True, verbose_name="fecha de constitución")
    actividad_economica = models.CharField(max_length=250, null=True, blank=True)
    pagina_web = models.CharField(max_length=250, null=True, blank=True)
    observaciones = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True


TIPOS_CLIENTE = (
    (1, 'Persona Natural'),
    (2, 'Persona Jurídica'),
)


class Cliente(baseCliente, Persona, Empresa):
    NATURAL = 1
    JURIDICO = 2

    tipo = models.PositiveSmallIntegerField(verbose_name="Tipo de cliente", choices=TIPOS_CLIENTE, null=True)

    class Meta:
        unique_together = ('tipo_identificacion', 'numero_identificacion')

    def __str__(self):
        if self.tipo == 1:
            return self.full_name()
        if self.tipo == 2:
            return self.razon_social
        else:
            return super().__str__()

    def full_name(self):
        if self.tipo == 1:
            return " ".join([self.primer_nombre or '', self.segundo_nombre or '', self.primer_apellido or '',
                             self.segundo_apellido or ''])
        if self.tipo == 2:
            return self.razon_social

    def to_json(self):
        o = super().to_json()
        if self.id:
            o['full_name'] = self.full_name()
            o['tipo'] = self.get_tipo_display()
            o['tipo_identificacion'] = self.get_tipo_identificacion_display()
            o['departamento'] = try_json(self.departamento, Departamento)
            o['municipio'] = try_json(self.municipio, Municipio)
        return o

    def polizas(self):
        return Poliza.objects.filter(cliente=self)


class ManagerNatural(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo=1)


class ClienteNatural(Cliente):
    objects = ManagerNatural()

    class Meta:
        proxy = True
        verbose_name = "persona natural"
        verbose_name_plural = "personas naturales"

    def save(self, *args, **kwargs):
        self.tipo = 1
        super().save(*args, **kwargs)


class ManagerJuridico(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo=2)


class ClienteJuridico(Cliente):
    objects = ManagerJuridico()

    class Meta:
        proxy = True
        verbose_name = "persona jurídica"
        verbose_name_plural = "personas jurídicas"

    def save(self, *args, **kwargs):
        self.tipo = 2
        self.tipo_identificacion = 4
        super().save(*args, **kwargs)


class Contacto(base):
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    aseguradora = models.ForeignKey(Aseguradora, null=True, on_delete=models.CASCADE)
    primer_nombre = models.CharField(max_length=45, null=True)
    segundo_nombre = models.CharField(max_length=45, null=True)
    primer_apellido = models.CharField(max_length=45, null=True)
    segundo_apellido = models.CharField(max_length=45, null=True)
    telefono = models.CharField(max_length=8, null=True)
    puesto = models.CharField(max_length=45, null=True)
    email_principal = models.EmailField(max_length=200, null=True)

    def full_name(self):
        return " ".join([self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido])

    def __str__(self):
        return self.full_name()


# endregion


class Tramite(base):
    code = models.CharField(max_length=25, null=True, blank=True, verbose_name="número")
    tipo_tramite = models.CharField(max_length=25, null=True, blank=True, choices=(
        ('endoso', 'Endoso'),
        ('nueva', 'Póliza nueva'),
        ('renovacion', 'Renovación'),
        ('cancelacion', 'Cancelación'),
    ))
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    poliza = models.ForeignKey('Poliza', null=True, blank=True, on_delete=models.SET_NULL)
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.TextField(max_length=1000, null=True, blank=True)
    estado = models.CharField(max_length=150, null=True, blank=True, choices=(
        ('proceso', 'En proceso'),
        ('documentacion', 'Pendiente de documentacion'),
        ('finalizado', 'Finalizado'),
        ('anulado', 'Anulado'),
    ))
    history = HistoricalRecords()

    def __str__(self):
        return "%s %s" % (self.tipo_tramite, self.cliente)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_code(self)
        super().save(*args, **kwargs)


class Campana(base):
    nombre = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "campaña"


class Vendedor(base):
    nombre = models.CharField(max_length=200, null=True)
    porcentaje_comision = models.FloatField(default=0.0)
    porcentaje_sub_comision = models.FloatField(default=0.0)
    porcentaje_retencion = models.FloatField(default=0.0)
    total_comision = models.FloatField(default=0.0)
    email = models.EmailField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Grupo(base):
    '''
        Póliza agrupadora
    '''
    fecha_expedicion = models.DateField(null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    aseguradora = models.ForeignKey(Aseguradora, null=True, on_delete=models.CASCADE, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    sub_ramo = models.ForeignKey(SubRamo, null=True, on_delete=models.CASCADE)
    nombre_grupo = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre_grupo

    def polizas(self):
        return Poliza.objects.filter(grupo=self)


class Poliza(base):
    TIPOS = (
        (1, 'Individual'),
        (2, 'Colectiva'),
    )
    ESTADOS = (
        ('1', 'Nueva'),
        ('2', 'Renovada'),
        ('3', 'No renovada'),
        ('4', 'Cancelada por no tomada'),
        ('5', 'Cancelada por falta de pago'),
        ('6', 'Anulada'),
    )
    tipo = models.PositiveSmallIntegerField(verbose_name="tipo póliza", null=True, blank=True,
                                            choices=TIPOS, default=1)
    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.SET_NULL, blank=True)
    numero_poliza = models.CharField(max_length=100, null=True, unique=True)
    estado_poliza = models.CharField(max_length=100, null=True, choices=ESTADOS)
    es_renovable = models.BooleanField(default=False)
    aseguradora = models.ForeignKey(Aseguradora, null=True, on_delete=models.CASCADE)
    sub_ramo = models.ForeignKey(SubRamo, null=True, on_delete=models.CASCADE,
                                 verbose_name="ramo")
    fecha_expedicion = models.DateField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE,
                                related_name="contratante_poliza", blank=True)
    beneficiaro_oneroso = models.BooleanField(default=False)
    observaciones_internas = models.TextField(max_length=500, null=True, blank=True)
    observaciones_cliente = models.TextField(max_length=500, null=True, blank=True)
    tipo_moneda = models.PositiveIntegerField(null=True)
    prima_neta = models.FloatField(default=0.0)
    derecho_emision = models.FloatField(default=0.0)
    recargo_descuento = models.FloatField(default=0.0, blank=True)
    iva = models.FloatField(default=0.0)
    otros = models.FloatField(default=0.0, blank=True)
    prima_total = models.FloatField(default=0.0)
    porcentaje_comision = models.FloatField(default=0.0, blank=True)
    monto_comision = models.FloatField(default=0.0, blank=True)
    comision_agencia = models.FloatField(default=0.0, blank=True)
    monto_agencia = models.FloatField(default=0.0, blank=True)
    correo_poliza_vencer = models.BooleanField(default=False)
    correo_cartera_vencer = models.BooleanField(default=False)
    sms_poliza_vencer = models.BooleanField(default=False)
    sms_cartera_vencer = models.BooleanField(default=False)
    forma_pago = models.CharField(max_length=45)
    metodo_pago = models.CharField(max_length=45)
    banco = models.CharField(max_length=45, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'póliza'

    def __str__(self):
        return self.numero_poliza

    def endosos(self):
        return Endoso.objects.filter(poliza=self)

    def cesionarios(self):
        return Cesionario.objects.filter(poliza=self)

    def primer_cesionario(self):
        if self.cesionarios().count() > 0:
            return self.cesionarios()[0].cliente
        else:
            return ""

    def certificados(self):
        return Certificado.objects.filter(poliza=self)

    def to_json(self):
        o = super().to_json()
        o['cliente'] = try_json(self.cliente, Cliente)
        o['aseguradora'] = try_json(self.aseguradora, Aseguradora)
        o['sub_ramo'] = try_json(self.sub_ramo, SubRamo)
        return o


class Certificado(base):
    numero = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=65, null=True, blank=True,
                            choices=(
                                ('edificio', 'Edificio'),
                                ('auto', 'Automovil'),
                                ('persona', 'Persona'),
                            ))
    poliza = models.ForeignKey(Poliza, null=True, on_delete=models.CASCADE)
    suma_asegurada = models.FloatField(default=0.0)

    # Edificio
    ubicacion = models.TextField(max_length=500, null=True, blank=True)

    # Auto
    marca = models.CharField(max_length=65, null=True, blank=True)
    modelo = models.CharField(max_length=65, null=True, blank=True)
    placa = models.CharField(max_length=65, null=True, blank=True)
    anno = models.CharField(max_length=65, null=True, blank=True)
    motor = models.CharField(max_length=65, null=True, blank=True)
    chasis = models.CharField(max_length=65, null=True, blank=True)

    # Persona
    primer_nombre = models.CharField(max_length=250, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=250, null=True, blank=True)
    primer_apellido = models.CharField(max_length=250, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=250, null=True, blank=True)

    tipo_persona = models.CharField(max_length=60, null=True, blank=True,
                                    choices=(
                                        ('titular', 'Titular'),
                                        ('dependiente', 'Dependiente'),
                                    ))
    parentesco = models.CharField(max_length=65, null=True, blank=True,
                                  choices=(
                                      ('Papa', 'Papa'),
                                      ('Mama', 'Mama'),
                                      ('Conyuge', 'Conyuge'),
                                      ('Hijo', 'Hijo'),
                                      ('Hija', 'Hija'),
                                  ))
    cedula = models.CharField(max_length=14, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def full_name(self):
        if self.tipo == "persona":
            return " ".join([
                self.primer_nombre or "",
                self.segundo_nombre or "",
                self.primer_apellido or "",
                self.segundo_apellido or "",
            ])
        else:
            return ""

    def __str__(self):
        return str(self.numero)


class Asegurado(base):
    poliza = models.ForeignKey(Poliza, null=True, related_name="asegurados_poliza", on_delete=models.CASCADE)
    certificado = models.CharField(max_length=255, null=True)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.cliente.full_name()


class Beneficiario(base):
    poliza = models.ForeignKey(Poliza, null=True, on_delete=models.CASCADE)
    tipo_beneficiario = models.CharField(max_length=100, null=True)
    primer_nombre = models.CharField(max_length=45, null=True)
    segundo_nombre = models.CharField(max_length=45, null=True)
    primer_apellido = models.CharField(max_length=45, null=True)
    segundo_apellido = models.CharField(max_length=45, null=True)
    tipo_identificacion = models.CharField(max_length=45, null=True)
    numero_identificacion = models.CharField(max_length=45, null=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)

    def full_name(self):
        return " ".join([self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido])

    def __str__(self):
        return self.full_name()


class calendarioPago(base):
    poliza = models.ForeignKey(Poliza, null=True, on_delete=models.CASCADE)
    numero_cuota = models.PositiveIntegerField(null=True)
    fecha_pago = models.DateField(null=True)
    valor_pago = models.FloatField(default=0.0)

    def __str__(self):
        return "%s - %s" % (self.poliza.numero_poliza, str(self.valor_pago))


class Endoso(base):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    tramite = models.ForeignKey(Tramite, null=True, blank=True, on_delete=models.SET_NULL)
    recibo_prima = models.CharField(max_length=45, null=True)
    tipo_endoso = models.CharField(max_length=45, null=True, choices=(
        ('Altas', 'Altas'),
        ('Bajas', 'Bajas'),
        ('Aumentos', 'Aumentos'),
        ('Disminución', 'Disminución'),
        ('Reclamos', 'Reclamos'),
        ('Renovaciones', 'Renovaciones'),
        ('Nueva', 'Nueva'),
    ))
    descripcion = models.TextField(max_length=400, null=True)
    fecha_emision = models.DateField(null=True)
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)
    comision = models.FloatField(default=30.0)
    prima_neta = models.FloatField(default=0.0)
    derecho_emision = models.FloatField(default=0.0)
    bomberos = models.FloatField(default=0.0)
    recargo_descuento = models.FloatField(verbose_name='Recargo/Descuento', default=0.0)
    iva = models.FloatField(default=0.0)
    otros = models.FloatField(default=0.0)
    prima_total = models.FloatField(default=0.0)
    forma_pago = models.CharField(max_length=150, null=True)
    cuotas = models.PositiveSmallIntegerField(default=1)
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    poliza = models.ForeignKey(Poliza, null=True, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, null=True, blank=True,
                              choices=(
                                  ('proceso', 'En proceso'),
                                  ('documentacion', 'Pendiente de documentacion'),
                                  ('finalizado', 'Finalizado'),
                                  ('anulado', 'Anulado'),
                              ))

    def __str__(self):
        return self.recibo_prima

    def aseguradora(self):
        return self.poliza.aseguradora.nombre

    aseguradora.short_description = "compañia"

    def contratante(self):
        return self.poliza.cliente.full_name()

    contratante.short_description = "cliente"


class Cesionario(base):
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    poliza = models.ForeignKey(Poliza, null=True, on_delete=models.CASCADE)
    monto_cesionado = models.FloatField(default=0.0)


class catalogoArchivo(base):
    nombre = models.CharField(max_length=45, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Archivo(base):
    nombre = models.CharField(max_length=250, null=True)
    catalogo = models.ForeignKey(catalogoArchivo, null=True, on_delete=models.CASCADE)
    tiene_caducidad = models.BooleanField(default=False)
    fecha_caducidad = models.DateField(null=True)
    archivo = models.FileField(upload_to="archivos", null=True, blank=True)
    type = models.ForeignKey(ContentType, null=True, blank=Tramite, on_delete=models.CASCADE)
    key = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.nombre

