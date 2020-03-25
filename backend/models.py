from django.db import models
from grappelli_extras.models import base, BaseEntity, get_code
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from .numero_letra import numero_a_letras
from image_cropping import ImageRatioField
from constance import config
from datetime import date
from utils.models import Departamento, Municipio, Direccion
from django.contrib import messages
import json
from django.urls import reverse, resolve
from django.utils.html import mark_safe
from django.contrib.contenttypes.models import ContentType


class Base(base):
    def to_json(self):
        o = super().to_json()
        o['str'] = str(self)
        return o

    class Meta:
        abstract = True


def get_media_url(model, filename):
    clase = model.__class__.__name__
    code = str(model.id)
    filename = filename.encode('utf-8')
    return '%s/%s/%s' % (clase, code, filename)


def get_profile(user):
    try:
        p, created = Cliente.objects.get_or_create(user=user)
        return p
    except:
        return None


def valid_date(year, month, day):
    valid = False
    while valid == False:
        try:
            return datetime(year=year, month=month, day=day)
        except:
            day -= 1


def json_object(obj, tpe):
    if obj:
        return obj.to_json()
    else:
        return tpe().to_json()


User.add_to_class('profile', get_profile)


# region Aseguradora


class Quincena(object):
    """
        Objeto auxiciliar para el calculo y muestra de las quincenas en el método de pago
    """
    MESES = [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre',
    ]

    def __init__(self, date, number):
        self.date = date
        self.year = date.year
        self.month = date.month
        self.number = number

    def __str__(self):
        if self.number == 1:
            return "Primera quincena de %s %s" % (self.MESES[self.month - 1], str(self.year))
        if self.number == 2:
            return "Segunda quincena de %s %s" % (self.MESES[self.month - 1], str(self.year))

    def add(self, qty):
        part = qty % 2
        qtym = (qty - part) / 2
        months = qtym % 12
        month = int(months) + self.month
        if month > 12:
            month = month - 12
        years = (qtym - months) / 12
        date = datetime(year=int(self.year + years), month=month, day=self.date.day)
        return Quincena(date=date, number=self.number + part)


class Aseguradora(BaseEntity, Base):
    ruc = models.CharField(max_length=14, null=True, blank=True)
    logo = models.ImageField(upload_to="empresas/logos", null=True, blank=True)
    cropping = ImageRatioField('logo', '400x400', allow_fullsize=True, verbose_name="vista previa")
    phone = models.CharField(max_length=80, verbose_name="teléfono de contacto", null=True, blank=True)
    email = models.EmailField(max_length=165, verbose_name="email de contacto", null=True, blank=True)
    address = models.TextField(max_length=600, verbose_name="dirección", null=True, blank=True)
    emision = models.FloatField(default=2.0, verbose_name="derecho de emision")

    def depreciar(self, valor_nuevo, anno):
        today = datetime.now()
        antiguedad = today.year - int(anno)
        if antiguedad < 0:
            antiguedad = 0
        tabla = self.tabla_depreciacion.all()[0]
        factor = tabla.annos.filter(antiguedad=antiguedad)[0].factor
        return round((valor_nuevo * factor), 2)

    def depreciar_post(self, request):
        print(request.POST)
        valor_nuevo = float(request.POST.get('valor_nuevo'))
        anno = int(request.POST.get('anno'))
        today = datetime.now()
        antiguedad = today.year - int(anno)
        if antiguedad < 0:
            antiguedad = 0
        tabla = self.tabla_depreciacion.all()[0]
        factor = tabla.annos.filter(antiguedad=antiguedad)[0].factor
        return round((valor_nuevo * factor), 2)

    def contactos(self):
        return ContactoAseguradora.objects.filter(aseguradora=self)


class ContactoAseguradora(Base):
    aseguradora = models.ForeignKey(Aseguradora, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=355)

    def __str__(self):
        return self.name


class Depreciacion(Base):
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE, related_name="tabla_depreciacion")

    def __str__(self):
        return self.aseguradora.name

    class Meta:
        verbose_name_plural = "Tablas de Depreciación"
        verbose_name = "tabla"


class Anno(Base):
    depreciacion = models.ForeignKey(Depreciacion, on_delete=models.CASCADE, related_name="annos")
    antiguedad = models.PositiveSmallIntegerField(default=0)
    factor = models.FloatField(default=0.0)

    def __str__(self):
        return "%s" % str(self.antiguedad)

    class Meta:
        verbose_name = "año"
        verbose_name_plural = "Años de antiguedad"


class Referencia(Base):
    marca = models.CharField(max_length=65)
    modelo = models.CharField(max_length=65)
    tipo = models.CharField(max_length=165, null=True)
    clase = models.CharField(max_length=165, null=True)
    anno = models.PositiveSmallIntegerField(verbose_name="año")
    valor = models.FloatField(default=0.0)
    chasis = models.CharField(max_length=125, null=True, blank=True)
    motor = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        verbose_name = "valor"
        verbose_name_plural = "valores de referencia"

    def __str__(self):
        return "%s, %s" % (self.marca, self.modelo)


class Marca(Base):
    marca = models.CharField(max_length=65)
    porcentaje_deducible = models.FloatField(default=0.25,
                                             help_text="usar formato decimar. Ejemplo 0.05 = 5%")
    minimo = models.FloatField(default=200.0)
    rotura_vidrios = models.FloatField(default=50.0)

    def __str__(self):
        return self.marca

    def porcentaje(self):
        return str(round(self.porcentaje_deducible * 100, 0)).replace('.0', '%')

    class Meta:
        verbose_name_plural = "marcas con recargo"


# endregion


# region Cliente


class TipoDoc:
    CEDULA = 1
    PASAPORTE = 2
    RESIDENTE = 3
    OTRO = 4

    @classmethod
    def choices(cls):
        return (cls.CEDULA, "Cédula"), (cls.PASAPORTE, "Pasaporte"), (cls.RESIDENTE, "Cédula de residente"), \
               (cls.OTRO, "Otro")


class TipoCliente:
    NATURAL = 1
    JURIDICO = 2

    @classmethod
    def choices(cls):
        return (cls.NATURAL, "Persona Natural"), (cls.JURIDICO, "Persona Jurídica")


class EstadoCliente:
    PROSPECTO = 1
    ACTIVO = 2
    INACTIVO = 3

    @classmethod
    def choices(cls):
        return (cls.PROSPECTO, "Prospecto"), (cls.ACTIVO, "Activo"), (cls.INACTIVO, "Inactivo")


class GeneroCliente:
    MASCULINO = 'M'
    FEMENINO = 'F'

    @classmethod
    def choices(cls):
        return (cls.MASCULINO, 'Masculino'), (cls.FEMENINO, 'Femenino')


class EstadoCivil:
    SOLTERO = 1
    CASADO = 2
    UNION_LIBRE = 3

    @classmethod
    def choices(cls):
        return (cls.SOLTERO, "Soltero"), (cls.CASADO, "Casado"), (cls.UNION_LIBRE, "Union de hecho libre")


class Persona(Base):
    """
        clase abstracta que representa una persona natural
    """
    cedula = models.CharField(max_length=14, null=True, blank=True, verbose_name="número de identificación")
    primer_nombre = models.CharField(max_length=125, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=125, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=125, null=True, blank=True,
                                        verbose_name="primer apellido")
    apellido_materno = models.CharField(max_length=125, null=True, blank=True,
                                        verbose_name="segundo apellido")
    genero = models.CharField(max_length=1, choices=GeneroCliente.choices(), null=True, blank=True)
    celular = models.CharField(max_length=8, null=True, blank=True)
    email_personal = models.EmailField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='perfiles', null=True, blank=True)
    estado_civil = models.PositiveSmallIntegerField(null=True, blank=True, choices=EstadoCivil.choices())
    cropping = ImageRatioField('foto', '400x400')

    def foto_perfil(self):
        if self.foto:
            return self.foto.url
        else:
            return "#"

    @property
    def nombres(self):
        return "%s %s" % (self.primer_nombre or "", self.segundo_nombre or "")

    @property
    def apellidos(self):
        return "%s %s" % (self.apellido_paterno or "", self.apellido_materno or "")

    @property
    def full_name(self):
        return "%s %s %s %s" % (self.primer_nombre or "", self.segundo_nombre or "",
                                self.apellido_paterno or "", self.apellido_materno or "")

    class Meta:
        abstract = True


class Empresa(Base):
    razon_social = models.CharField(max_length=250, null=True, blank=True)
    nombre_comercial = models.CharField(max_length=250, null=True, blank=True)
    ruc = models.CharField(max_length=14, null=True, blank=True, verbose_name="número de identificación")
    fecha_constitucion = models.DateField(null=True, blank=True, verbose_name="fecha de constitución")
    actividad_economica = models.CharField(max_length=250, null=True, blank=True, verbose_name="actividad económica")
    pagina_web = models.CharField(max_length=250, null=True, blank=True, verbose_name="página web")
    observaciones = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True


class Entidad(BaseEntity, Base):
    descuento = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "entidades"


class Cliente(Persona, Empresa, Direccion):
    '''
        Esta clase se convertirá en el cliente de trustseguros
    '''
    nombre = models.CharField(max_length=600, null=True, blank=True)
    tipo_identificacion = models.PositiveSmallIntegerField(choices=TipoDoc.choices(), default=TipoDoc.CEDULA, null=True,
                                                           blank=True)
    tipo_cliente = models.PositiveIntegerField(default=TipoCliente.NATURAL,
                                               choices=TipoCliente.choices(), blank=True)
    estado_cliente = models.PositiveIntegerField(choices=EstadoCliente.choices(), null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cambiar_pass = models.BooleanField(default=False, verbose_name="Exigir cambio de contraseña")

    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="cliente_empresa_referencia")
    contacto = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="cliente_contacto_referencia")
    representante = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="cliente_representante_legal")
    sucursal = models.CharField(max_length=125, null=True, blank=True)
    codigo_empleado = models.CharField(max_length=25, null=True, blank=True)
    cargo = models.CharField(max_length=125, null=True, blank=True)
    es_cesionario = models.BooleanField(default=False)

    class Meta:
        verbose_name = "cliente"

    def __str__(self):
        if self.tipo_cliente == TipoCliente.NATURAL:
            return self.full_name
        else:
            return self.razon_social

    def perfil_completo(self):
        return (self.primer_nombre and self.apellido_paterno and \
                self.cedula and self.departamento and self.municipio and \
                self.celular and self.codigo_empleado)

    def polizas_activas(self):
        return Poliza.objects.filter(user=self.user, tramite__isnull=True)

    def contactos(self):
        return Contacto.objects.filter(contacto=self)

    def polizas(self):
        return Poliza.objects.filter(cliente=self)

    def tramites(self):
        return Ticket.objects.filter(cliente=self)

    def edad(self):
        try:
            today = date.today()
            year = self.cedula[7:9]
            if (int(year) > 30):
                year = "19%s" % year
            else:
                year = "20%s" % year

            nacimiento = date(year=int(year), month=int(self.cedula[5:7]), day=int(self.cedula[3:5]))
            return today.year - nacimiento.year - (
                    (today.month, today.day) < (nacimiento.month, nacimiento.day))
        except:
            return "desconocida"

    def dependientes_sepelio(self):
        return benSepelio.objects.filter(empleado=self, tramite__isnull=True)

    def dependientes_accidente(self):
        return benAccidente.objects.filter(empleado=self, tramite__isnull=True)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(args, kwargs)

    def dar_de_baja(self, request):
        u = self.user
        u.is_active = False
        u.save()
        messages.info(request, 'Usuario inactivado con éxito')

    def save(self, *args, **kwargs):
        if self.tipo_cliente == TipoCliente.NATURAL:
            self.nombre = self.full_name
        if self.tipo_cliente == TipoCliente.JURIDICO:
            self.nombre = self.razon_social
        super().save(*args, **kwargs)


class ManagerProspecto(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(estado_cliente=EstadoCliente.PROSPECTO)


class ClienteProspecto(Cliente):
    objects = ManagerProspecto()

    def save(self, *args, **kwargs):
        self.estado_cliente = EstadoCliente.PROSPECTO
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "prospecto"


class ManagerNatural(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo_cliente=TipoCliente.NATURAL, estado_cliente=EstadoCliente.ACTIVO)


class ClienteNatural(Cliente):
    objects = ManagerNatural()

    def save(self, *args, **kwargs):
        self.estado_cliente = EstadoCliente.ACTIVO
        self.tipo_cliente = TipoCliente.NATURAL
        self.name = self.full_name
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "persona natural"
        verbose_name_plural = "clientes"


class ManagerJuridico(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo_cliente=TipoCliente.JURIDICO, estado_cliente=EstadoCliente.ACTIVO)


class ClienteJuridico(Cliente):
    objects = ManagerJuridico()

    def save(self, *args, **kwargs):
        self.estado_cliente = EstadoCliente.ACTIVO
        self.tipo_cliente = TipoCliente.JURIDICO
        self.name = self.razon_social
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "persona jurídica"
        verbose_name_plural = "clientes"


class ManagerContacto(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo_cliente=TipoCliente.NATURAL,
                                             contacto__isnull=False)


class Contacto(Cliente):
    objects = ManagerContacto()

    def save(self, *args, **kwargs):
        self.tipo_cliente = TipoCliente.NATURAL
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = "contacto"


# endregion


# region Poliza


class Moneda(Base):
    moneda = models.CharField(max_length=50)

    def __str__(self):
        return self.moneda


class Grupo(Base):
    name = models.CharField(max_length=65, verbose_name="nombre")

    def __str__(self):
        return self.name


class Ramo(Base):
    name = models.CharField(max_length=65, verbose_name="nombre")

    def __str__(self):
        return self.name


class SubRamo(Base):
    ramo = models.ForeignKey(Ramo, on_delete=models.CASCADE)
    name = models.CharField(max_length=65, verbose_name="nombre")

    def __str__(self):
        return self.name

    def to_json(self):
        o = super().to_json()
        try:
            o['ramo'] = self.ramo.to_json()
        except:
            o['ramo'] = {'id': '', 'name': ''}
        return o


class CampoAdicional(Base):
    sub_ramo = models.ForeignKey(SubRamo, on_delete=models.CASCADE, related_name="datos_tecnicos",
                                 null=True)
    name = models.CharField(max_length=65, verbose_name="nombre")
    label = models.CharField(max_length=65, verbose_name="etiqueta")

    def __str__(self):
        return self.name


class TipoCobertura:
    BASICA = 1
    AMPLIA = 2
    ADICIONAL = 3
    OPCIONAL = 4

    @classmethod
    def choices(cls):
        return (cls.BASICA, 'Básica'), (cls.AMPLIA, 'Amplia'), (cls.ADICIONAL, 'Adicional'), (cls.OPCIONAL, 'Opcional')


class TipoCalculo:
    PRECIO_FIJO = 1
    TASA_PORCENTUAL = 2
    TASA_PORMILLAR = 3

    @classmethod
    def choices(cls):
        return (cls.PRECIO_FIJO, 'PRECIO FIJO'), (cls.TASA_PORCENTUAL, 'TASA PORCENTUAL'), \
               (cls.TASA_PORMILLAR, 'TASA PORMILLAR'),


class TipoExceso:
    CERO = '0.0'
    VALOR_NUEVO = 'valor_nuevo'
    VALOR_DEPRECIADO = 'valor_depreciado'
    OTRO = 'otro'

    @classmethod
    def choices(cls):
        return (cls.CERO, '0.0'), (cls.VALOR_NUEVO, 'Valor de Nuevo'), (cls.VALOR_DEPRECIADO, 'Valor Depreciado'), \
               (cls.OTRO, 'Otro'),


class FormaPago:
    CONTADO = 1
    CREDITO = 2

    @classmethod
    def choices(cls):
        return (cls.CONTADO, "Contado"), (cls.CREDITO, "Fraccionado")


class MedioPago:
    TRANSFERENCIA = 1
    CHEQUE = 2
    DEPOSITO = 3
    NOMINA = 4
    PRESTAMO = 5
    TARJETA_CREDITO = 6

    @classmethod
    def choices(cls):
        return (cls.TRANSFERENCIA, 'Transferencia'), (cls.CHEQUE, 'Cheques'), (cls.DEPOSITO, 'Depositos'), \
               (cls.TARJETA_CREDITO, 'Tarjeta de Credito')


class EstadoPoliza:
    PENDIENTE = 0
    ACTIVA = 1
    VENCIDA = 2
    RENOVADA = 3
    CANCELADA = 4
    ANULADA = 5
    OTRO = 6

    @classmethod
    def choices(cls):
        return (cls.PENDIENTE, "Pendiente"), (cls.ACTIVA, "Activa"), (cls.VENCIDA, "Vencida"), (
            cls.RENOVADA, "Renovada"), \
               (cls.CANCELADA, "Cancelada"), (cls.ANULADA, "Anulada"), (cls.OTRO, "Otro")


class TipoPoliza:
    INDIVIDUAL = 1
    COLECTIVA = 2

    @classmethod
    def choices(cls):
        return (cls.INDIVIDUAL, "Individual"), (cls.COLECTIVA, "Colectiva")


class ConceptoPoliza:
    NUEVA = 1
    RENOVACION = 2

    @classmethod
    def choices(cls):
        return (cls.NUEVA, 'Nueva Póliza'), (cls.RENOVACION, 'Renovación')


class Cobertura(Base):
    sub_ramo = models.ForeignKey(SubRamo, on_delete=models.CASCADE, related_name="coberturas")
    name = models.CharField(max_length=75, null=True, verbose_name="nombre")
    description = models.TextField(max_length=1500, null=True, blank=True,
                                   verbose_name="Descripción detallada")
    tipo_calculo = models.PositiveSmallIntegerField(choices=TipoCalculo.choices(), default=3)
    tipo_cobertura = models.PositiveSmallIntegerField(choices=TipoCobertura.choices(), default=1,
                                                      verbose_name="tipo de cobertura")
    tipo_exceso = models.CharField(max_length=25, choices=TipoExceso.choices(), default='0.0',
                                   verbose_name="variable de referencia")
    iva = models.BooleanField(default=True, verbose_name="aplica iva")

    def __str__(self):
        return self.name

    def get_precio(self, aseguradora):
        try:
            return Precio.objects.get(aseguradora=aseguradora, cobertura=self)
        except:
            return None

    def to_json(self):
        o = super().to_json()
        o['precios'] = [x.to_json() for x in self.precios.all()]
        return o

    class Meta:
        verbose_name_plural = "coberturas ofrecidas"
        verbose_name = "cobertura"
        ordering = ('id',)


class DetalleCobertura(Base):
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    monto = models.FloatField(default=0.0)


class Precio(Base):
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE, related_name="precios")
    valor = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.cobertura.name, self.aseguradora.name)


class Poliza(Base):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    tipo_poliza = models.PositiveSmallIntegerField(choices=TipoPoliza.choices(), default=TipoPoliza.INDIVIDUAL,
                                                   null=True)
    grupo = models.ForeignKey(Grupo, null=True, on_delete=models.SET_NULL, blank=True)
    ramo = models.ForeignKey(Ramo, null=True, on_delete=models.SET_NULL, blank=True)
    sub_ramo = models.ForeignKey(SubRamo, null=True, on_delete=models.SET_NULL, blank=True)

    fecha_emision = models.DateField(null=True, blank=True, verbose_name="fecha de inicio vigencia")
    fecha_vence = models.DateField(null=True, blank=True, verbose_name="fecha fin de vigencia")
    fecha_pago = models.DateField(null=True, blank=True)
    code = models.CharField(max_length=25, null=True, blank=True)
    no_poliza = models.CharField(max_length=25, null=True, blank=True, verbose_name="número de póliza")
    no_recibo = models.CharField(max_length=25, null=True, blank=True, verbose_name="número de recibo")
    concepto = models.PositiveSmallIntegerField(choices=ConceptoPoliza.choices(), default=ConceptoPoliza.NUEVA,
                                                null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="polizas_automovil")
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="polizas_automovil_cliente")
    contratante = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="polizas_automovil_contratante")
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True, on_delete=models.SET_NULL)
    referencia = models.ForeignKey(Referencia, null=True, blank=True, on_delete=models.SET_NULL)
    tipo_cobertura = models.CharField(max_length=165, null=True, blank=True,
                                      choices=TipoCobertura.choices())
    estado_poliza = models.PositiveSmallIntegerField(null=True, blank=True, default=EstadoPoliza.PENDIENTE,
                                                     choices=EstadoPoliza.choices())

    nombres = models.CharField(max_length=165, null=True, blank=True, verbose_name="nombre")
    apellidos = models.CharField(max_length=165, null=True, blank=True)
    cedula = models.CharField(max_length=14, null=True, blank=True)
    celular = models.CharField(max_length=8, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    domicilio = models.TextField(max_length=400, null=True, blank=True)

    card_number = models.CharField(max_length=40, null=True, blank=True)
    card_expiry = models.CharField(max_length=40, null=True, blank=True)
    card_type = models.CharField(max_length=40, null=True, blank=True)

    marca = models.CharField(max_length=65, null=True, blank=True)
    porcentaje_deducible = models.FloatField(default=0.2, null=True, blank=True,
                                             help_text="usar formato decimar. Ejemplo 0.05 = 5%")
    porcentaje_deducible_extension = models.FloatField(default=0.3, null=True, blank=True,
                                                       help_text="usar formato decimar. Ejemplo 0.05 = 5%")
    minimo_deducible = models.FloatField(default=100.0, null=True, blank=True, )
    minimo_deducible_extension = models.FloatField(default=100.0, null=True, blank=True, )
    deducible_rotura_vidrios = models.FloatField(default=0.0, null=True, blank=True, )
    modelo = models.CharField(max_length=65, null=True, blank=True)
    anno = models.PositiveSmallIntegerField(verbose_name="año", null=True, blank=True, )
    chasis = models.CharField(max_length=65, null=True, blank=True)
    motor = models.CharField(max_length=65, null=True, blank=True)
    circulacion = models.CharField(max_length=65, null=True, blank=True)
    placa = models.CharField(max_length=65, null=True, blank=True)
    color = models.CharField(max_length=65, null=True, blank=True)

    moneda = models.ForeignKey(Moneda, null=True, on_delete=models.SET_NULL, blank=True)
    costo_exceso = models.FloatField(default=0.0, null=True, blank=True)
    monto_exceso = models.FloatField(default=0.0, null=True, blank=True)
    valor_nuevo = models.FloatField(default=0.0, null=True, blank=True)
    suma_asegurada = models.FloatField(default=0.0, null=True, blank=True, verbose_name="suma asegurada total")
    subtotal = models.FloatField(default=0.0, null=True, blank=True)
    descuento = models.FloatField(default=0.0, null=True, blank=True)
    emision = models.FloatField(default=0.0, null=True, blank=True)
    iva = models.FloatField(default=0.0, null=True, blank=True)
    otros = models.FloatField(default=0.0, null=True, blank=True)
    total = models.FloatField(default=0.0, null=True, blank=True)

    per_comision = models.FloatField(default=0.0, verbose_name="% comisión", null=True, blank=True, )
    amount_comision = models.FloatField(default=0.0, verbose_name="total comisión", null=True, blank=True, )

    cesion_derecho = models.BooleanField(default=False, verbose_name="¿tiene cesión de derecho?")
    beneficiario = models.ForeignKey(Entidad, null=True, blank=True, on_delete=models.SET_NULL)
    cesioinario = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)

    forma_pago = models.CharField(max_length=25, default="anual", null=True, blank=True, )
    f_pago = models.PositiveIntegerField(choices=FormaPago.choices(), null=True, blank=True,
                                         verbose_name="forma de pago")
    medio_pago = models.CharField(max_length=25, null=True, blank=True,
                                  choices=(
                                      ('debito_automatico', 'Débito automático'),
                                      ('deduccion_nomina', 'Deducción de nómina'),
                                      ('deposito_referenciado', 'Depósito referenciado'),
                                  ))
    m_pago = models.PositiveIntegerField(choices=MedioPago.choices(), null=True, blank=True,
                                         verbose_name="medio de pago", )
    cuotas = models.PositiveIntegerField(default=1, null=True, blank=True, )
    monto_cuota = models.FloatField(default=0.0, null=True, blank=True, )
    moneda_cobro = models.CharField(max_length=3, null=True, blank=True)
    banco_emisor = models.CharField(max_length=25, null=True, blank=True)

    file_circulacion = models.FileField(upload_to=get_media_url, null=True, blank=True)
    file_cedula = models.FileField(upload_to=get_media_url, null=True, blank=True)
    file_carta = models.FileField(upload_to=get_media_url, null=True, blank=True)

    tramite = models.ForeignKey('Tramite', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="ticket_de_baja")

    notificado = models.BooleanField(default=False)

    total_pagos = models.FloatField(default=0.0)

    editable = models.BooleanField(default=True)
    perdir_comentarios = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Pólizas"
        verbose_name = "póliza"
        permissions = (
            ("report_debito_automatico", "report_debito_automatico"),
            ("report_cotizaciones", "report_cotizaciones"),
            ("reporte_deduccion_nomina", "reporte_deduccion_nomina"),
            ("reporte_polizas_vencer", "reporte_polizas_vencer"),
        )

    def data_load(self):
        try:
            return json.loads(self.extra_data)
        except:
            return {}

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_code(self, 6)
        if not self.fecha_pago and self.fecha_emision:
            self.fecha_pago = datetime(year=self.fecha_emision.year, month=self.fecha_emision.month,
                                       day=self.fecha_emision.day) + timedelta(days=10)
        super(Poliza, self).save(*args, **kwargs)

    def print_code(self):
        return 'AS - %s' % self.code

    def __str__(self):
        if self.no_poliza:
            return str(self.no_poliza)
        else:
            return "sin número"

    @property
    def trust_url(self):
        return reverse('trustseguros:polizas')

    @property
    def dias_vigencia(self):
        if (self.fecha_emision and self.fecha_vence) and (self.fecha_emision < self.fecha_vence):
            hoy = datetime.now()
            emision = datetime(year=self.fecha_emision.year, month=self.fecha_emision.month, day=self.fecha_emision.day)
            vencimiento = datetime(year=self.fecha_vence.year, month=self.fecha_vence.month, day=self.fecha_vence.day)
            return (vencimiento - hoy).days
        else:
            return None

    @property
    def media_files(self):
        return Archivo.media_files(self)

    @property
    def bitacora(self):
        return Comentario.bitacora(self)

    @property
    def ver(self):
        tag = '<a class="btn" href="%s#%s">Ver</a>' % (self.trust_url, self.id)
        return mark_safe(tag)

    @property
    def estado(self):
        return self.get_estado_poliza_display()

    def to_json(self):
        o = super().to_json()
        o['code'] = self.print_code()
        o['cliente'] = json_object(self.cliente, Cliente)
        o['aseguradora'] = json_object(self.aseguradora, Aseguradora)
        o['ramo'] = json_object(self.ramo, Ramo)
        o['grupo'] = json_object(self.grupo, Grupo)
        o['dias_vigencia'] = self.dias_vigencia
        o['tipo_poliza'] = {'value': self.tipo_poliza, 'label': self.get_tipo_poliza_display()}
        o['estado_poliza'] = {'value': self.estado_poliza, 'label': self.get_estado_poliza_display()}
        return o

    def saldo(self):
        try:
            return round(self.total - self.monto_cuota, 2)
        except:
            return 0.0

    def tabla_pago(self):
        cuotas = []
        if self.forma_pago == 'mensual':
            anno = self.fecha_pago.year
            mes = self.fecha_pago.month
            dia = self.fecha_pago.day
            for i in range(1, self.cuotas + 1):
                if mes != 12:
                    mes += 1
                else:
                    mes = 1
                    anno += 1
                fecha = valid_date(year=anno, month=mes, day=dia)
                cuotas.append({'numero': i, 'cuotas': self.cuotas, 'fecha': fecha, 'monto': self.monto_cuota})
        return cuotas

    def tabla_pagos(self):
        total = self.total
        fecha_pago = datetime(year=self.fecha_pago.year, month=self.fecha_pago.month, day=self.fecha_pago.day)
        cuotas = self.cuotas
        monto_cuota = round(total / cuotas, 2)
        data = []
        anno = fecha_pago.year
        mes = fecha_pago.month
        dia = fecha_pago.day
        data.append({'numero': 1, 'cuotas': cuotas, 'fecha': fecha_pago.strftime('%d/%m/%Y'), 'monto': monto_cuota,
                     'estado': 'VIGENTE'})
        for i in range(1, cuotas):
            if mes != 12:
                mes += 1
            else:
                mes = 1
                anno += 1
            fecha = valid_date(year=anno, month=mes, day=dia)
            data.append({'numero': i + 1, 'cuotas': cuotas, 'fecha': fecha.strftime('%d/%m/%Y'), 'monto': monto_cuota,
                         'estado': 'VIGENTE'})
        return data

    def fecha_vencimiento(self):
        self.fecha_vence = date(year=self.fecha_emision.year, month=self.fecha_emision.month,
                                day=self.fecha_emision.day) + timedelta(days=365)
        self.save()
        return self.fecha_vence

    def is_renovable(self):
        return (self.fecha_vencimiento() - date.today()).days <= 30
        # return True

    def print_cuotas(self):
        return numero_a_letras(self.cuotas)

    def valor_prima(self):
        try:
            return round(float(self.subtotal) - (config.SOA_AUTOMOVIL + float(self.costo_exceso)), 2)
        except:
            return 0.0

    @property
    def prima_neta(self):
        try:
            return round(self.subtotal - self.descuento, 2)
        except:
            return 0.0

    def rotura_vidrios(self):
        try:
            return round(float(self.valor_nuevo) * 0.05, 2)
        except:
            return 0.0

    def suma_asegurada_letras(self):
        return numero_a_letras(self.suma_asegurada)

    def nombre_asegurado(self):
        return "%s %s" % (self.nombres or "", self.apellidos or "")

    def vehiculo(self):
        return "%s %s %s" % (self.marca or "", self.modelo or "", str(self.anno) or "")

    def porcentaje(self):
        return str(round(float(self.porcentaje_deducible) * 100, 0)).replace('.0', '%')

    def porcentaje_extension(self):
        return str(round(float(self.porcentaje_deducible_extension) * 100, 0)).replace('.0', '%')

    def minimo(self):
        return str(round(float(self.minimo_deducible), 2))

    def deducible(self):
        return "%s Mínimo U$ %s" % (
            self.porcentaje(),
            self.minimo()
        )

    def deducible_extension(self):
        return "%s Mínimo U$ %s" % (
            self.porcentaje_extension(),
            self.minimo()
        )

    def monto_exceso_ampliado(self):
        return float(self.monto_exceso) * 2

    def primera_quincena(self):
        if self.fecha_emision.day <= 13:
            return Quincena(date=self.fecha_emision, number=1)
        else:
            return Quincena(date=self.fecha_emision, number=2)

    def ultima_quincena(self):
        return self.primera_quincena().add(self.cuotas)

    def coberturas(self):
        return CoberturaPoliza.objects.filter(poliza=self)


class EstadoPago:
    ANULADO = 0
    VIGENTE = 1
    VENCIDO = 2
    PAGADO = 3

    @classmethod
    def choices(cls):
        return (cls.ANULADO, "Anulado"), (cls.VIGENTE, "Vigente"), (cls.VENCIDO, "Vencido"), (cls.PAGADO, "Pagado")


class Pago(Base):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE,
                               related_name="pagos")
    monto = models.FloatField(default=0.0)
    numero = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_vence = models.DateField(null=True)
    fecha_pago = models.DateField(null=True)
    estado = models.PositiveSmallIntegerField(choices=EstadoPago.choices(), null=True, blank=True,
                                              default=EstadoPago.VIGENTE)

    class Meta:
        ordering = ['fecha_vence', ]


class CoberturaPoliza(Base):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    monto = models.FloatField(default=0.0)


class DatoPoliza(base):
    """
    Modelo usado para generar los formularios dinamicos de acuerdo al subramo de la poliza
    """
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE, related_name="datos_tecnicos")

    extra_data = models.CharField(max_length=1000000, null=True, blank=True,
                                  verbose_name="datos técnicos")


class TipoTramite:
    ENDOSO = 1
    CANCELACION = 2
    CESION = 3
    CORRECCION = 4
    COTIZACION = 5
    CAMBIO = 6
    LAVADO = 7
    RECLAMO = 8
    RENOVACION = 9
    LIQUIDACION = 10

    @classmethod
    def choices(cls):
        return (cls.ENDOSO, "Endoso por póliza"), (cls.CANCELACION, "Cancelación de póliza"), \
               (cls.CESION, "Cesión de derechos"), (cls.CORRECCION, "Corección de póliza"), \
               (cls.COTIZACION, "Cotización nueva póliza"), (cls.CAMBIO, "Cambio de razón social"), \
               (cls.LAVADO, "Documento de lavado de dinero"), (cls.RECLAMO, "Documento de reclamo"), \
               (cls.RENOVACION, "Renovaciones"), (cls.LIQUIDACION, "Liquidaciones")


class Tramite(Base):
    tipo_tramite = models.PositiveSmallIntegerField(choices=TipoTramite.choices(), null=True)

    contacto_aseguradora = models.ForeignKey(ContactoAseguradora, null=True, on_delete=models.SET_NULL, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fechahora = models.DateTimeField(null=True)
    prioridad = models.PositiveIntegerField(choices=(
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ), default=2)
    vence = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=55, null=True, blank=True, default="Pendiente",
                              choices=(
                                  ('Pendiente', 'Pendiente'),
                                  ('En Proceso', 'En Proceso'),
                                  ('Finalizado', 'Finalizado'),
                              ))
    code = models.CharField(max_length=10, null=True, blank=True, verbose_name="número")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='ticketes')
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='tickets_cliente')
    poliza = models.ForeignKey(Poliza, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="poliza_resultante")
    descripcion = models.TextField(max_length=600, null=True, blank=True)

    nombres = models.CharField(max_length=165, null=True, blank=True)
    apellidos = models.CharField(max_length=165, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    cedula = models.CharField(max_length=14, null=True, blank=True)
    celular = models.CharField(max_length=8, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    domicilio = models.TextField(max_length=400, null=True, blank=True)

    referente = models.CharField(max_length=125, null=True, blank=True,
                                 choices=(
                                     ("auto", "Auto"),
                                     ("sepelio", "Sepelio"),
                                     ("accidente", "Accidente"),
                                     ("otro", "Otro"),
                                 ))

    movimiento = models.CharField(max_length=125, null=True, blank=True, choices=(
        ('1', 'Solicitar cambios en la Póliza'),
        ('2', 'Dar de baja'),
        ('3', 'Problemas de cobranza'),
        ('4', 'Quiero asesoría'),
        ('5', 'Aperturar un reclamo'),
        ('6', 'Error en la página'),
        ('7', 'No encuentro mi seguro'),
        ('8', 'Otro'),
    ))

    motivo = models.CharField(max_length=125, null=True, blank=True, choices=(
        ('1', 'Por venta'),
        ('2', 'Ya no quiero mi seguro'),
        ('3', 'Cancelación de prestamo'),
    ))

    marca = models.CharField(max_length=65, null=True, blank=True)
    modelo = models.CharField(max_length=65, null=True, blank=True)
    anno = models.PositiveSmallIntegerField(verbose_name="año", null=True, blank=True)
    chasis = models.CharField(max_length=65, null=True, blank=True)
    motor = models.CharField(max_length=65, null=True, blank=True)
    circulacion = models.FileField(upload_to="cotizaciones", null=True, blank=True)
    placa = models.CharField(max_length=65, null=True, blank=True)
    color = models.CharField(max_length=65, null=True, blank=True)
    uso = models.CharField(max_length=65, null=True, blank=True)

    valor_nuevo = models.FloatField(default=0.0)
    suma_asegurada = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)
    emision = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_code(self, 6)
        super().save(*args, **kwargs)

    def valor_prima(self):
        return self.subtotal - 55

    def rotura_vidrios(self):
        return round(float(self.valor_nuevo) * 0.05, 2)

    def get_vence(self):
        now = datetime.now()
        if not self.vence:
            self.vence = self.created + timedelta(days=1)
            self.save()
        vence = datetime(
            year=self.vence.year,
            month=self.vence.month,
            day=self.vence.day,
            hour=self.vence.hour,
            minute=self.vence.minute,
            second=self.vence.second
        )
        num = (vence - now).total_seconds()
        if num > 0:
            hor = int(num / 3600)
            minu = int((num - (hor * 3600)) / 60)
            seg = int(num - ((hor * 3600) + (minu * 60)))
            return "%s:%s:%s" % (str(hor).zfill(2), str(minu).zfill(2), str(seg).zfill(2))
        return "<span>00:00:00</span> <button class='btn-trust btn-trust-sm contacto-directo' data-ticket='%s'>Contacto directo</button>" \
               % self.id

    def to_json(self):
        o = super().to_json()
        if self.poliza:
            o['poliza'] = {'id': self.poliza.id, 'number': self.poliza.no_poliza}
        else:
            o['poliza'] = {'id': '', 'number': ''}
        if self.user:
            o['user'] = {'id': self.user.id, 'username': self.user.username}
        else:
            o['user'] = {'id': '', 'username': ''}
        if self.cliente:
            o['cliente'] = {'id': self.cliente.id, 'name': self.cliente.__str__()}
        else:
            o['cliente'] = {'id': '', 'name': ''}
        return o

    class Meta:
        verbose_name = "Trámite"


class benAbstract(Base):
    created = models.DateTimeField(auto_now_add=True, null=True)
    numero_poliza = models.CharField(max_length=30, null=True, blank=True, verbose_name="Número de Póliza")
    orden = models.ForeignKey('OrdenTrabajo', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="orden_%(class)s")
    empleado = models.ForeignKey(Cliente, on_delete=models.CASCADE,
                                 related_name="beneficiarios_%(class)s")
    parentesco = models.CharField(max_length=65, null=True, blank=True,
                                  choices=(
                                      ('PADRE', 'Padre'),
                                      ('MADRE', 'Madre'),
                                      ('HERMANO', 'Hermano'),
                                      ('HERMANA', 'Hermana'),
                                      ('CONYUGE', 'Cónyuge'),
                                      ('HIJO', 'Hijo'),
                                      ('HIJA', 'Hija'),
                                  ))
    primer_nombre = models.CharField(max_length=125, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=125, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=125, null=True, blank=True)
    apellido_materno = models.CharField(max_length=125, null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    suma_asegurada = models.FloatField(null=True, blank=True)
    tipo_identificacion = models.CharField(max_length=25, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tramite = models.ForeignKey(Tramite, null=True, blank=True, on_delete=models.SET_NULL)
    file_cedula = models.FileField(upload_to='cedulas', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "beneficiarios"
        verbose_name = "beneficiario"

    def full_name(self):
        return "%s %s %s %s" % (self.primer_nombre or "", self.segundo_nombre or "",
                                self.apellido_paterno or "", self.apellido_materno or "")

    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def fecha_vencimiento(self):
        return datetime(day=self.created.day, month=self.created.month, year=self.created.year) + \
               timedelta(days=365)


class benSepelio(benAbstract):

    def save(self, *args, **kwargs):
        if not self.numero_poliza:
            self.numero_poliza = config.POLIZA_SEPELIO_DEPENDIENTE
        if not self.costo:
            self.costo = config.COSTO_SEPELIO
        if not self.suma_asegurada:
            self.suma_asegurada = config.SUMA_SEPELIO
        super(benSepelio, self).save(*args, **kwargs)


class benAccidente(benAbstract):
    prima = models.FloatField(default=0.0)
    carnet = models.FloatField(default=0.0)
    emision = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.numero_poliza:
            self.numero_poliza = config.POLIZA_ACCIDENTE
        if not self.suma_asegurada:
            self.suma_asegurada = config.SUMA_ACCIDENTE_DEPENDIENTE
        super(benAccidente, self).save(*args, **kwargs)


# endregion


# region Tramite


class OrdenTrabajo(BaseEntity, Base):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tipo = models.CharField(max_length=3, choices=(
        ('CF', 'Sepelio'),
        ('AP', 'Accidente'),
    ), default='CF')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True, on_delete=models.SET_NULL)

    def beneficiarios(self):
        if self.tipo == "CF":
            return benSepelio.objects.filter(orden=self)
        if self.tipo == "AP":
            return benAccidente.objects.filter(orden=self)

    def nomeclatura(self):
        return "%s-%s" % (self.tipo, self.code)

    def __str__(self):
        return self.nomeclatura()

    class Meta:
        verbose_name_plural = "ordenes de trabajo"


class Sucursal(BaseEntity, Base):
    pass


class Analitics(Base):
    created = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=100, null=True, blank=True)
    paso = models.PositiveSmallIntegerField(null=True, blank=True)
    data = models.TextField(max_length=1000, null=True, blank=True)


class Notificacion(Base):
    poliza = models.ForeignKey(Poliza, null=True, blank=True, on_delete=models.CASCADE)
    benaccidente = models.ForeignKey(benAccidente, null=True, blank=True, on_delete=models.CASCADE)
    bensepelio = models.ForeignKey(benSepelio, null=True, blank=True, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=True, blank=True)


# endregion


class Archivo(base):
    created = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="archivo_user_created")
    updated = models.DateTimeField(auto_now=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="archivo_user_updated")

    nombre = models.CharField(max_length=250, null=True)
    tiene_caducidad = models.BooleanField(default=False)
    fecha_caducidad = models.DateField(null=True)
    archivo = models.FileField(upload_to="archivos", null=True, blank=True)
    type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    key = models.PositiveIntegerField(null=True)

    @classmethod
    def media_files(cls, obj):
        return Archivo.objects.filter(type=ContentType.objects.get(
            app_label='backend', model=obj._meta.model_name
        ), key=obj.id).order_by('-updated')

    def __str__(self):
        return self.nombre

    def to_json(self):
        o = super().to_json()
        o['created'] = self.created
        o['updated'] = self.updated
        o['created_user'] = {'id': self.created_user.id, 'username': self.created_user.username}
        o['updated_user'] = {'id': self.updated_user.id, 'username': self.updated_user.username}
        return o


class Comentario(base):
    created = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="comentario_user_created")
    updated = models.DateTimeField(auto_now=True)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="comentario_user_updated")
    comentario = models.CharField(max_length=500, null=True)
    type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    key = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.comentario

    @classmethod
    def bitacora(cls, obj):
        return Comentario.objects.filter(type=ContentType.objects.get(
            app_label='backend', model=obj._meta.model_name
        ), key=obj.id)

    def to_json(self):
        o = super().to_json()
        o['created'] = self.created
        o['updated'] = self.updated
        o['created_user'] = {'id': self.created_user.id, 'username': self.created_user.username}
        o['updated_user'] = {'id': self.updated_user.id, 'username': self.updated_user.username}
        return o
