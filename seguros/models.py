from django.db import models
from grappelli_extras.models import base, BaseEntity
from image_cropping import ImageRatioField
from django.utils.timezone import now as today
from django.db.models import Count
from datetime import datetime, timedelta

TIPO_AUTO = (
    (1, 'VEHICULO'),
    (2, 'MOTO'),
)

TIPO_COBERTURA = (
    (1, 'Básica'),
    (2, 'Ampliada'),
    (3, 'Adicional'),
    (4, 'Opcional'),
)

TIPO_CALCULO = (
    (1, 'PRECIO FIJO'),
    (2, 'TASA PORCENTUAL'),
    (3, 'TASA PORMILLAR'),
)

TIPO_EXCESO = (
    ('0.0', '0.0'),
    ('valor_nuevo', 'Valor de Nuevo'),
    ('valor_depreciado', 'Valor Depreciado'),
    ('otro', 'Otro'),
)


MODOS_PAGO = (
    (1, 'UN PAGO ANUAL'),
    (2, '12 CUOTAS MENSUALES'),
)


MEDIOS_PAGO = (
    (1, 'DÉBITO AUTOMÁTICO'),
    (2, 'DEPÓSITO REFERENCIADO'),
)


def _get_number(model, length=4):
    model_class = type(model)
    qs = model_class.objects.all()
    if qs.count() > 0:
        try:
            return str(int(qs.aggregate(models.Max('number'))['number__max']) + 1).zfill(length)
        except:
            return str(1).zfill(length)
    else:
        return str(1).zfill(length)


def porcentual(sumaAsegurada, tasa):
    return (sumaAsegurada * tasa) / 100.00


def pormillar(sumaAsegurada, tasa):
    return (sumaAsegurada * tasa) / 1000.00


def calcular_exceso(sumaAsegurada, tipo_calculo, tasa):
    if tipo_calculo == 2:
        return porcentual(sumaAsegurada, tasa)
    if tipo_calculo == 3:
        return pormillar(sumaAsegurada, tasa)
    else:
        return tasa


class Aseguradora(BaseEntity):
    logo = models.ImageField(upload_to="empresas/logos", null=True, blank=True)
    cropping = ImageRatioField('logo', '400x400', allow_fullsize=True, verbose_name="vista previa")
    phone = models.CharField(max_length=80, verbose_name="teléfono de contacto", null=True, blank=True)
    address = models.TextField(max_length=600, verbose_name="dirección", null=True, blank=True)
    emision = models.FloatField(default=2.0, verbose_name="derecho de emision")

    def depreciar(self, valor_nuevo, anno, tipo_vehiculo):
        antiguedad = today().year - int(anno)
        if antiguedad < 0:
            antiguedad = 0
        tabla = self.tabla_depreciacion.get(tipo_auto=tipo_vehiculo)
        factor = tabla.annos.filter(antiguedad=antiguedad)[0].factor
        return round((valor_nuevo * factor), 2)


class Depreciacion(base):
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE, related_name="tabla_depreciacion")
    tipo_auto = models.PositiveSmallIntegerField(choices=TIPO_AUTO, default=1)

    def __str__(self):
        return self.aseguradora.name

    class Meta:
        verbose_name_plural = "Tablas de Depreciación"
        verbose_name = "tabla"
        unique_together = ('aseguradora', 'tipo_auto')


class Anno(base):
    depreciacion = models.ForeignKey(Depreciacion, on_delete=models.CASCADE, related_name="annos")
    antiguedad = models.PositiveSmallIntegerField(default=0)
    factor = models.FloatField(default=0.0)

    def __str__(self):
        return "%s" % str(self.antiguedad)

    class Meta:
        verbose_name = "año"
        verbose_name_plural = "Años de antiguedad"


class Producto(BaseEntity):
    description = models.TextField(max_length=1500, null=True, blank=True,
                                   verbose_name="Descripción detallada")

    def coberturas_basicas(self):
        return Cobertura.objects.filter(producto=self, tipo_cobertura=1)

    def coberturas_ampliadas(self):
        return Cobertura.objects.filter(producto=self, tipo_cobertura__in=[1, 2])

    def coberturas_adicionales(self):
        return Cobertura.objects.filter(producto=self, tipo_cobertura=3)

    def coberturas_opcionales(self):
        return Cobertura.objects.filter(producto=self, tipo_cobertura=4)

    def calcular(self, cobertura, aseguradora, monto):
        precio = Precio.objects.get(cobertura=cobertura, aseguradora=aseguradora)
        if precio.available:
            if cobertura.tipo_calculo == 1:
                return precio.valor
            if cobertura.tipo_calculo == 2:
                return (precio.valor * monto) / 100
            if cobertura.tipo_calculo == 3:
                return (precio.valor * monto) / 1000
        else:
            return 0.0


class Cobertura(BaseEntity):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="coberturas")
    description = models.TextField(max_length=1500, null=True, blank=True,
                                   verbose_name="Descripción detallada")
    tipo_calculo = models.PositiveSmallIntegerField(choices=TIPO_CALCULO, default=3)
    tipo_cobertura = models.PositiveSmallIntegerField(choices=TIPO_COBERTURA, default=1,
                                                      verbose_name="variable de cobertura")
    tipo_exceso = models.CharField(max_length=25, choices=TIPO_EXCESO, default='0.0',
                                   verbose_name="variable de calculo")
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


class DetalleCobertura(base):
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    monto = models.FloatField(default=0.0)


class Precio(base):
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE, related_name="precios")
    valor = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.cobertura.name, self.aseguradora.name)


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


class Cotizacion(base):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number = models.CharField(max_length=6, null=True) # fixme pendiente como se va ha generar
    aseguradora = models.ManyToManyField(Aseguradora, verbose_name="aseguradoras")
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    nombres = models.CharField(max_length=300)
    apellidos = models.CharField(max_length=300, null=True)
    cedula = models.CharField(max_length=14, null=True, verbose_name="cédula")
    email = models.EmailField(max_length=300, null=True)
    tipo_auto = models.PositiveSmallIntegerField(choices=TIPO_AUTO, default=1)
    marca = models.CharField(max_length=65, null=True)
    modelo = models.CharField(max_length=65, null=True)
    anno = models.PositiveSmallIntegerField(null=True, verbose_name="año")
    chasis = models.CharField(max_length=125, null=True, blank=True)
    motor = models.CharField(max_length=125, null=True, blank=True)
    valor_nuevo = models.FloatField(default=0.0, verbose_name="valor de nuevo")

    def __str__(self):
        return self.number

    def suma_asegurada(self):
        return [x.to_json() for x in self.depreciaciones.all()]

    def to_json(self):
        o = super().to_json()
        o['aseguradora'] = [x.to_json() for x in self.aseguradora.all()]
        o['suma_asegurada'] = self.suma_asegurada()
        return o

    def crear_depreciacion(self):
        for a in self.aseguradora.all():
            v, created = ValorDepreciado.objects.get_or_create(cotizacion=self, aseguradora=a)
            v.annos = today().year - self.anno
            v.valor_nuevo = self.valor_nuevo
            v.valor_depreciado = a.depreciar(self.valor_nuevo, self.anno, self.tipo_auto)
            v.save()

    def costos_cotizacion(self):
        return self.costos.all().order_by('id')

    def costos_adicionales(self):
        return self.costos.filter(cobertura__in=self.producto.coberturas_adicionales()).order_by('id')

    def costos_basicos(self):
        return self.costos.filter(cobertura__in=self.producto.coberturas_basicas()).order_by('id')

    class Meta:
        verbose_name = "cotización"
        verbose_name_plural = "cotizaciónes"

    def save(self, *args, **kwargs):
        try:
            int(self.number)
        except:
            self.number = _get_number(self)
        super(Cotizacion, self).save(*args, **kwargs)
        self.crear_depreciacion()


class Costo(base):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="costos")
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1500, null=True, blank=True,
                                   verbose_name="Descripción detallada")
    suma_asegurada = models.FloatField(default=0.0, verbose_name="exceso")
    tipo_exceso = models.CharField(max_length=25, choices=TIPO_EXCESO, default='0.0',
                                   verbose_name="variable de calculo")
    tipo_calculo = models.PositiveSmallIntegerField(choices=TIPO_CALCULO, default=3)
    iva = models.BooleanField(default=True, verbose_name="aplica iva")


class Oferta(base):
    costo = models.ForeignKey(Costo, on_delete=models.CASCADE, related_name="ofertas")
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    tasa = models.FloatField(default=0.0)
    quota_seguro = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)


class ValorDepreciado(base):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="depreciaciones")
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    annos = models.PositiveSmallIntegerField(default=0, verbose_name="años")
    valor_nuevo = models.FloatField(default=0.0)
    valor_depreciado = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('cotizacion', 'aseguradora')

    def to_json(self):
        o = super().to_json()
        o['aseguradora'] = self.aseguradora.to_json()
        return o



class Poliza(base):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number = models.CharField(max_length=25, null=True) # fixme pendiente como se va ha generar
    aseguradora = models.ForeignKey(Aseguradora, null=True, blank=True, on_delete=models.CASCADE)

    nombres = models.CharField(max_length=300)
    apellidos = models.CharField(max_length=300, null=True)
    cedula = models.CharField(max_length=14, null=True, verbose_name="cédula")
    telefono = models.CharField(max_length=14, null=True, verbose_name="teléfono")
    email = models.EmailField(max_length=300, null=True)

    tipo_auto = models.PositiveSmallIntegerField(choices=TIPO_AUTO, default=1)
    marca = models.CharField(max_length=65, null=True)
    modelo = models.CharField(max_length=65, null=True)
    anno = models.PositiveSmallIntegerField(null=True, verbose_name="año")
    capacidad = models.CharField(max_length=65, null=True)
    tonelaje = models.CharField(max_length=65, null=True)
    chasis = models.CharField(max_length=125, null=True, blank=True)
    motor = models.CharField(max_length=125, null=True, blank=True)
    circulacion = models.CharField(max_length=125, null=True, blank=True)
    vin = models.CharField(max_length=125, null=True, blank=True)
    certificado = models.CharField(max_length=125, null=True, blank=True)
    placa = models.CharField(max_length=125, null=True, blank=True)
    uso = models.CharField(max_length=125, null=True, blank=True)

    valor_nuevo = models.FloatField(default=0.0, verbose_name="valor de nuevo")
    valor_depreciado = models.FloatField(default=0.0, verbose_name="valor de nuevo")

    basica = models.FloatField(default=0.0)
    amplia = models.FloatField(default=0.0)
    adicional = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)
    emision = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    cuota = models.FloatField(default=0.0)
    modo_pago = models.PositiveSmallIntegerField(choices=MODOS_PAGO, default=1)
    medios_pago = models.PositiveSmallIntegerField(choices=MEDIOS_PAGO, default=1)

    def __str__(self):
        return self.number

    @property
    def desde(self):
        return self.created

    @property
    def hasta(self):
        return self.created + timedelta(days=365)


class Beneficio(base):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE, related_name="beneficios")
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1500, null=True, blank=True,
                                   verbose_name="Descripción detallada")
    suma_asegurada = models.FloatField(default=0.0, verbose_name="exceso")
    emision = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)

# class Banpro(base):
#     cedula = models.CharField(max_length=14)
#     cliente = models.CharField(max_length=255)
#     poliza = models.CharField(max_length=25)
#     dueno = models.CharField(max_length=255)
#     vence = models.DateField(null=True)
#     aseguradora = models.CharField(max_length=14)
#     email = models.CharField(max_length=255)
#     casa = models.CharField(max_length=400, verbose_name="direccion casa")
#     trabajo = models.CharField(max_length=14, verbose_name="direccion trabajo")
#     telefono = models.CharField(max_length=14)
#     celular = models.CharField(max_length=14)
#     otro = models.CharField(max_length=14)
#     # datos del vehiculo
#     motor = models.CharField(max_length=50)
#     chasis = models.CharField(max_length=50)
#     modelo = models.CharField(max_length=50)
#     anno = models.CharField(max_length=50)
#     marca = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name = "cliente"
#         verbose_name_plural = "clientes banpro"

def aplicar_producto(producto, cotizacion):
    for cobertura in producto.coberturas.all().order_by('id'):
        costo, created = Costo.objects.get_or_create(cotizacion=cotizacion, cobertura=cobertura)
        costo.name = cobertura.name
        costo.description = cobertura.description
        costo.tipo_exceso = cobertura.tipo_exceso
        costo.tipo_calculo = cobertura.tipo_calculo
        costo.iva = cobertura.iva
        costo.save()
        for aseguradora in cotizacion.aseguradora.all():
            precio = cobertura.get_precio(aseguradora)
            oferta, created = Oferta.objects.get_or_create(costo=costo, aseguradora=aseguradora)
            oferta.tasa = precio.valor
            oferta.available = precio.available
            if cobertura.tipo_calculo == 1:
                oferta.quota_seguro = precio.valor
            oferta.save()


def _prepare_marca(marca):
    return (marca['marca'], marca['marca'])


def _prepare_modelo(modelo):
    return (modelo['modelo'], modelo['modelo'])


def _prepare_annos(anno):
    return (str(anno), str(anno))


try:
    year = int(str(today().year))
    annos = range(year - 10, year + 2)
    annos = [_prepare_annos(a) for a in annos]
    marcas = Referencia.objects.values('marca').annotate(modelos=Count('modelo')).order_by('marca')
    modelos = Referencia.objects.values().values('modelo').annotate(Count('valor')).order_by('marca', 'modelo')
    marcas = [_prepare_marca(marca) for marca in marcas]
    modelos = [_prepare_modelo(modelo) for modelo in modelos]
except:

    annos = []
    marcas = []
    modelos = []
