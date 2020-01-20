from django.db import models
from grappelli_extras.models import base, BaseEntity, get_code
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from .numero_letra import numero_a_letras
from image_cropping import ImageRatioField
from constance import config
from datetime import date
from utils.models import Departamento, Municipio
from django.contrib import messages


def get_media_url(model, filename):
    clase = model.__class__.__name__
    code = str(model.id)
    filename = filename.encode('utf-8')
    return '%s/%s/%s' % (clase, code, filename)


def get_profile(user):
    try:
        p, created = PerfilEmpleado.objects.get_or_create(user=user)
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


User.add_to_class('profile', get_profile)


class Quincena(object):
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


class Aseguradora(BaseEntity):
    logo = models.ImageField(upload_to="empresas/logos", null=True, blank=True)
    cropping = ImageRatioField('logo', '400x400', allow_fullsize=True, verbose_name="vista previa")
    phone = models.CharField(max_length=80, verbose_name="teléfono de contacto", null=True, blank=True)
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


class Depreciacion(base):
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE, related_name="tabla_depreciacion")

    def __str__(self):
        return self.aseguradora.name

    class Meta:
        verbose_name_plural = "Tablas de Depreciación"
        verbose_name = "tabla"


class Anno(base):
    depreciacion = models.ForeignKey(Depreciacion, on_delete=models.CASCADE, related_name="annos")
    antiguedad = models.PositiveSmallIntegerField(default=0)
    factor = models.FloatField(default=0.0)

    def __str__(self):
        return "%s" % str(self.antiguedad)

    class Meta:
        verbose_name = "año"
        verbose_name_plural = "Años de antiguedad"


class Referencia(base):
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


class Marca(base):
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


class Entidad(BaseEntity):
    descuento = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "entidades"


class PerfilEmpleado(base):

    '''
        Esta clase se convertirá en el cliente de trustseguros

    '''


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    primer_nombre = models.CharField(max_length=125, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=125, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=125, null=True, blank=True)
    apellido_materno = models.CharField(max_length=125, null=True, blank=True)
    email_personal = models.EmailField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='perfiles', null=True, blank=True)
    cropping = ImageRatioField('foto', '400x400')
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, null=True, blank=True)
    cedula = models.CharField(max_length=14, null=True, blank=True)
    celular = models.CharField(max_length=8, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, null=True, blank=True, on_delete=models.CASCADE)
    domicilio = models.TextField(max_length=400, null=True, blank=True)
    sucursal = models.CharField(max_length=125, null=True, blank=True)
    codigo_empleado = models.CharField(max_length=25, null=True, blank=True)
    cargo = models.CharField(max_length=125, null=True, blank=True)
    cambiar_pass = models.BooleanField(default=False, verbose_name="Exigir cambio de contraseña")

    def __str__(self):
        return self.full_name

    def perfil_completo(self):
        return (self.primer_nombre and self.apellido_paterno and \
                self.cedula and self.departamento and self.municipio and \
                self.celular and self.codigo_empleado)

    def foto_perfil(self):
        if self.foto:
            return self.foto.url
        else:
            return "#"

    def polizas_activas(self):
        return Poliza.objects.filter(user=self.user, ticket__isnull=True)

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

    def dependientes_sepelio(self):
        return benSepelio.objects.filter(empleado=self, ticket__isnull=True)

    def dependientes_accidente(self):
        return benAccidente.objects.filter(empleado=self, ticket__isnull=True)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(args, kwargs)

    def dar_de_baja(self, request):
        u = self.user
        u.is_active = False
        u.save()
        messages.info(request, 'Usuario inactivado con éxito')


class Poliza(base):
    COBER_TYPES = (
        ('amplia', 'Cobertura amplia'),
        ('basica', 'Cobertura básica'),
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    fecha_emision = models.DateTimeField(null=True, blank=True)
    fecha_vence = models.DateTimeField(null=True, blank=True)
    fecha_pago = models.DateField(null=True, blank=True)
    code = models.CharField(max_length=25, null=True, blank=True)
    no_poliza = models.CharField(max_length=25, null=True, blank=True, default="pendiente")
    no_recibo = models.CharField(max_length=25, null=True, blank=True, default="pendiente")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="polizas_automovil")
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True, on_delete=models.SET_NULL)
    referencia = models.ForeignKey(Referencia, null=True, blank=True, on_delete=models.SET_NULL)
    tipo_cobertura = models.CharField(max_length=165, null=True, blank=True,
                                      choices=COBER_TYPES)

    nombres = models.CharField(max_length=165, null=True, blank=True)
    apellidos = models.CharField(max_length=165, null=True, blank=True)
    cedula = models.CharField(max_length=14, null=True, blank=True)
    celular = models.CharField(max_length=8, null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    domicilio = models.TextField(max_length=400, null=True, blank=True)

    card_number = models.CharField(max_length=40, null=True, blank=True)
    card_expiry = models.CharField(max_length=40, null=True, blank=True)
    card_type = models.CharField(max_length=40, null=True, blank=True)

    marca = models.CharField(max_length=65)
    porcentaje_deducible = models.FloatField(default=0.2,
                                             help_text="usar formato decimar. Ejemplo 0.05 = 5%")
    porcentaje_deducible_extension = models.FloatField(default=0.3,
                                                       help_text="usar formato decimar. Ejemplo 0.05 = 5%")
    minimo_deducible = models.FloatField(default=100.0)
    minimo_deducible_extension = models.FloatField(default=100.0)
    deducible_rotura_vidrios = models.FloatField(default=0.0)
    modelo = models.CharField(max_length=65)
    anno = models.PositiveSmallIntegerField(verbose_name="año")
    chasis = models.CharField(max_length=65, null=True, blank=True)
    motor = models.CharField(max_length=65, null=True, blank=True)
    circulacion = models.CharField(max_length=65, null=True, blank=True)
    placa = models.CharField(max_length=65, null=True, blank=True)
    color = models.CharField(max_length=65, null=True, blank=True)

    costo_exceso = models.FloatField(default=0.0)
    monto_exceso = models.FloatField(default=0.0)
    valor_nuevo = models.FloatField(default=0.0)
    suma_asegurada = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)
    emision = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    cesion_derecho = models.BooleanField(default=False)
    beneficiario = models.ForeignKey(Entidad, null=True, blank=True, on_delete=models.SET_NULL)

    forma_pago = models.CharField(max_length=25, default="anual")
    medio_pago = models.CharField(max_length=25, null=True, blank=True,
                                  choices=(
                                      ('debito_automatico', 'Débito automático'),
                                      ('deduccion_nomina', 'Deducción de nómina'),
                                      ('deposito_referenciado', 'Depósito referenciado'),
                                  ))
    cuotas = models.PositiveIntegerField(default=1)
    monto_cuota = models.FloatField(default=0.0)
    moneda_cobro = models.CharField(max_length=3, null=True, blank=True)
    banco_emisor = models.CharField(max_length=25, null=True, blank=True)

    file_circulacion = models.FileField(upload_to=get_media_url, null=True, blank=True)
    file_cedula = models.FileField(upload_to=get_media_url, null=True, blank=True)
    file_carta = models.FileField(upload_to=get_media_url, null=True, blank=True)

    ticket = models.ForeignKey('Ticket', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="ticket_de_baja")

    notificado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Pólizas Automovil"
        verbose_name = "póliza"
        permissions = (
            ("report_debito_automatico", "report_debito_automatico"),
            ("report_cotizaciones", "report_cotizaciones"),
            ("reporte_deduccion_nomina", "reporte_deduccion_nomina"),
            ("reporte_polizas_vencer", "reporte_polizas_vencer"),
        )

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
        return ""

    def to_json(self):
        o = super().to_json()
        o['code'] = self.print_code()
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


class Pago(base):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)
    monto = models.FloatField(default=0.0)
    fecha_vence = models.DateField(null=True)
    fecha_pago = models.DateField(null=True)


class Ticket(base):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vence = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=55, null=True, blank=True, default="Pendiente",
                              choices=(
                                  ('Pendiente', 'Pendiente'),
                                  ('En Proceso', 'En Proceso'),
                                  ('Finalizado', 'Finalizado'),
                              ))
    code = models.CharField(max_length=10, null=True, blank=True, verbose_name="número")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='ticketes')
    cliente = models.ForeignKey(PerfilEmpleado, null=True, blank=True, on_delete=models.SET_NULL, related_name='tickets_cliente')
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


class benAbstract(base):
    created = models.DateTimeField(auto_now_add=True, null=True)
    numero_poliza = models.CharField(max_length=30, null=True, blank=True, verbose_name="Número de Póliza")
    orden = models.ForeignKey('OrdenTrabajo', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="orden_%(class)s")
    empleado = models.ForeignKey(PerfilEmpleado, on_delete=models.CASCADE,
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
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
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


class OrdenTrabajo(BaseEntity):
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


class Sucursal(BaseEntity):
    pass


class Analitics(base):
    created = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=100, null=True, blank=True)
    paso = models.PositiveSmallIntegerField(null=True, blank=True)
    data = models.TextField(max_length=1000, null=True, blank=True)


class Notificacion(base):
    poliza = models.ForeignKey(Poliza, null=True, blank=True, on_delete=models.CASCADE)
    benaccidente = models.ForeignKey(benAccidente, null=True, blank=True, on_delete=models.CASCADE)
    bensepelio = models.ForeignKey(benSepelio, null=True, blank=True, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=True, blank=True)
