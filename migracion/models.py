from django.db import models
from grappelli_extras.models import base
import re
from django.utils.safestring import mark_safe


class Empleado(base):
    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    cedula = models.CharField(max_length=255, null=True, blank=True)
    correo = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    primer_nombre = models.CharField(max_length=255, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=255, null=True, blank=True)
    primer_apellido = models.CharField(max_length=255, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=255, null=True, blank=True)
    nombres = models.SmallIntegerField(null=True, blank=True)
    noblank = models.CharField(max_length=255, null=True, blank=True)
    reversed = models.CharField(max_length=255, null=True, blank=True)

    migrated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @staticmethod
    def username_exist(username):
        return len(Empleado.objects.filter(username=username)) > 0

    def _username(self):
        username = self.primer_nombre.lower() + self.primer_apellido.lower()
        if not self.username_exist(username):
            return username
        else:
            return ""

    def _nombres(self):
        return len(self.name.split(' '))

    def fill_nombres(self):
        names = self.name.split(' ')
        self.primer_nombre = names[0]
        self.segundo_nombre = names[1] + ' ' + names[2] + ' ' + names[3]
        self.primer_apellido = names[4]
        self.segundo_apellido = names[5]
        self.save()

    def _cedula(self):
        return self.cedula.replace('-', '')

    def _reversed(self):
        l = []
        if self.primer_apellido:
            l.append(self.primer_apellido)
        if self.segundo_apellido:
            l.append(self.segundo_apellido)
        if self.primer_nombre:
            l.append(self.primer_nombre)
        if self.segundo_nombre:
            l.append(self.segundo_nombre)
        return " ".join(l)

    class Meta:
        ordering = ['name', ]


class Auto(base):
    empleado = models.ForeignKey(Empleado, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="automoviles")
    contratante = models.CharField(max_length=250, null=True, blank=True)
    cedula = models.CharField(max_length=250, null=True, blank=True)
    poliza = models.CharField(max_length=250, null=True, blank=True)
    marca = models.CharField(max_length=250, null=True, blank=True)
    placa = models.CharField(max_length=250, null=True, blank=True)
    modelo = models.CharField(max_length=250, null=True, blank=True)
    anno = models.CharField(max_length=250, null=True, blank=True)
    chasis = models.CharField(max_length=250, null=True, blank=True)
    motor = models.CharField(max_length=250, null=True, blank=True)
    suma = models.FloatField(null=True, blank=True)
    prima = models.FloatField(null=True, blank=True)
    color = models.CharField(max_length=250, null=True, blank=True)
    inicio = models.CharField(max_length=250, null=True, blank=True)
    fin = models.CharField(max_length=250, null=True, blank=True)

    def por_cedula(self):
        try:
            return Empleado.objects.get(cedula=self.cedula)
        except:
            return None

    def por_nombre(self):
        try:
            return Empleado.objects.get(name=self.contratante)
        except:
            return None

    def _empleado(self):
        if self.empleado:
            return self.empleado
        else:
            try:
                html = '<ul>' \
                       + ''.join(
                    ['<li><a class="sugerencia" href="#" data-em="%s" data-id="%s">%s</a></li>' % (
                    e.id, self.id, e.name) for e in
                     Empleado.objects.filter(primer_nombre=self.contratante.split(' ')[0])]
                ) + '</ul>'
                return mark_safe(html)
            except:
                return None

    def asignar(self, request):
        self.empleado = Empleado.objects.get(id=request.POST.get('em'))
        self.save()


class Accidente(base):
    empleado = models.ForeignKey(Empleado, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="accidentes")
    asegurado = models.CharField(max_length=250, null=True, blank=True)
    cedula = models.CharField(max_length=250, null=True, blank=True)
    fechanacimiento = models.CharField(max_length=250, null=True, blank=True)
    edad = models.CharField(max_length=250, null=True, blank=True)
    parentesco = models.CharField(max_length=250, null=True, blank=True)
    titular = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    primer_nombre = models.CharField(max_length=255, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=255, null=True, blank=True)
    primer_apellido = models.CharField(max_length=255, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=255, null=True, blank=True)
    nombres = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.asegurado

    def _empleado(self):
        try:
            return Empleado.objects.get(name=self.asegurado)
        except:
            return None

    def _titular(self):
        if self.parentesco == 'TITULAR':
            return None
        else:
            try:
                id = self.id
                while True:
                    id = id - 1
                    t = Accidente.objects.get(id=id)
                    if t.parentesco == 'TITULAR':
                        return t
                    else:
                        print(t.asegurado)
            except:
                return None

    def _nombres(self):
        return len(self.asegurado.split(' '))

    def fill_nombres(self):
        if self.empleado and self.parentesco == 'TITULAR':
            self.primer_nombre = self.empleado.primer_nombre
            self.segundo_nombre = self.empleado.segundo_nombre
            self.primer_apellido = self.empleado.primer_apellido
            self.segundo_apellido = self.empleado.segundo_apellido
            self.save()
        if self.nombres == 4:
            self.primer_nombre = self.asegurado.split(' ')[0]
            self.segundo_nombre = self.asegurado.split(' ')[1]
            self.primer_apellido = self.asegurado.split(' ')[2]
            self.segundo_apellido = self.asegurado.split(' ')[3]
            self.save()
        if self.nombres == 5:
            self.primer_nombre = self.asegurado.split(' ')[0]
            self.segundo_nombre = self.asegurado.split(' ')[1] + " " + self.asegurado.split(' ')[2]
            self.primer_apellido = self.asegurado.split(' ')[3]
            self.segundo_apellido = self.asegurado.split(' ')[4]
            self.save()

    def sugerencia(self):
        if self.empleado:
            return self.empleado
        else:
            if self.parentesco == 'TITULAR':
                try:
                    html = '<ul>' \
                           + ''.join(
                        [
                            '<li><a class="sugerencia" href="#" data-em="%s" data-id="%s"  data-model="accidente">%s</a></li>' % (
                            e.id, self.id, e.name) for e in
                            Empleado.objects.filter(primer_nombre=self.asegurado.split(' ')[0])]
                    ) + '</ul>'
                    return mark_safe(html)
                except:
                    return None
            else:
                return None

    def asignar(self, request):
        self.empleado = Empleado.objects.get(id=request.POST.get('em'))
        self.save()


class Sepelio(base):
    ente = models.CharField(max_length=255, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="sepelios")
    asegurado = models.CharField(max_length=255, null=True, blank=True)
    desde = models.CharField(max_length=255, null=True, blank=True)
    hasta = models.CharField(max_length=255, null=True, blank=True)
    nacimiento = models.CharField(max_length=255, null=True, blank=True)
    edad = models.CharField(max_length=255, null=True, blank=True)
    suma = models.FloatField(null=True, blank=True)
    prima = models.FloatField(null=True, blank=True)
    parentesco = models.CharField(max_length=255, default="TITULAR")
    cedula = models.CharField(max_length=250, null=True, blank=True)

    primer_nombre = models.CharField(max_length=255, null=True, blank=True)
    segundo_nombre = models.CharField(max_length=255, null=True, blank=True)
    primer_apellido = models.CharField(max_length=255, null=True, blank=True)
    segundo_apellido = models.CharField(max_length=255, null=True, blank=True)
    nombres = models.SmallIntegerField(null=True, blank=True)

    inverted = models.BooleanField(default=False)

    def __str__(self):
        return self.asegurado

    def _empleado(self):
        try:
            return Empleado.objects.get(noblank=self.asegurado.replace(' ', '').replace(' ', ''))
        except:
            return None

    def _nombres(self):
        return len(self.asegurado.split(' '))

    def fill_nombres(self):
        if self.empleado and self.parentesco == 'TITULAR':
            self.primer_nombre = self.empleado.primer_nombre
            self.segundo_nombre = self.empleado.segundo_nombre
            self.primer_apellido = self.empleado.primer_apellido
            self.segundo_apellido = self.empleado.segundo_apellido
            self.save()
        if self.inverted:
            if self.nombres == 4:
                self.primer_nombre = self.asegurado.split(' ')[2]
                self.segundo_nombre = self.asegurado.split(' ')[3]
                self.primer_apellido = self.asegurado.split(' ')[0]
                self.segundo_apellido = self.asegurado.split(' ')[1]
                self.save()
            if self.nombres == 5:
                self.primer_nombre = self.asegurado.split(' ')[2]
                self.segundo_nombre = self.asegurado.split(' ')[3] + " " + self.asegurado.split(' ')[4]
                self.primer_apellido = self.asegurado.split(' ')[0]
                self.segundo_apellido = self.asegurado.split(' ')[1]
                self.save()
        else:
            if self.nombres == 4:
                self.primer_nombre = self.asegurado.split(' ')[0]
                self.segundo_nombre = self.asegurado.split(' ')[1]
                self.primer_apellido = self.asegurado.split(' ')[2]
                self.segundo_apellido = self.asegurado.split(' ')[3]
                self.save()
            if self.nombres == 5:
                self.primer_nombre = self.asegurado.split(' ')[0]
                self.segundo_nombre = self.asegurado.split(' ')[1] + " " + self.asegurado.split(' ')[2]
                self.primer_apellido = self.asegurado.split(' ')[3]
                self.segundo_apellido = self.asegurado.split(' ')[4]
                self.save()

    def sugerencias_por_nombre(self):
        return Empleado.objects.filter(primer_nombre=self.asegurado.split(' ')[0])

    def _inverted(self):
        if self.sugerencias_por_nombre().count() == 0:
            return True
        else:
            return False

    def sugerencia(self):
        if self.empleado:
            return self.empleado
        else:
            if self.parentesco == 'TITULAR':
                if not self.inverted:
                    try:
                        html = '<ul>' \
                               + ''.join(
                            [
                                '<li><a class="sugerencia" href="#" data-em="%s" data-id="%s" data-model="sepelio">%s</a></li>' % (
                                    e.id, self.id, e.name) for e in
                                Empleado.objects.filter(primer_nombre=self.asegurado.split(' ')[0])]
                        ) + '</ul>'
                        return mark_safe(html)
                    except:
                        return None
                else:
                    try:
                        html = '<ul>' \
                               + ''.join(
                            [
                                '<li><a class="sugerencia" href="#" data-em="%s" data-id="%s" data-model="sepelio">%s</a></li>' % (
                                    e.id, self.id, e.reversed) for e in
                                Empleado.objects.filter(primer_apellido=self.asegurado.split(' ')[0])]
                        ) + '</ul>'
                        return mark_safe(html)
                    except:
                        return None
            else:
                return None

    def asignar(self, request):
        self.empleado = Empleado.objects.get(id=request.POST.get('em'))
        self.save()

    def _nacimiento(self):
        if self.cedula and len(self.cedula) == 14:
            return "19%s-%s-%s" % (self.cedula[7:9], self.cedula[5:7], self.cedula[3:5],)
        else:
            return ""

    class Meta:
        ordering = ['asegurado', ]

    def save(self, *args, **kwargs):
        self.nombres = self._nombres()
        super().save(args, kwargs)


class DependienteSepelio(base):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    certificado = models.CharField(max_length=255, null=True, blank=True)
    ente = models.CharField(max_length=255, null=True, blank=True)
    certificado_dependiente = models.CharField(max_length=255, null=True, blank=True)
    nombre_dependiente = models.CharField(max_length=255, null=True, blank=True)
    parentesco = models.CharField(max_length=255, null=True, blank=True)
    cedula = models.CharField(max_length=255, null=True, blank=True)
    ente_dependiente = models.CharField(max_length=255, null=True, blank=True)

    titular = models.ForeignKey(Sepelio, null=True, blank=True, on_delete=models.CASCADE)

    def _titular(self):
        try:
            return Sepelio.objects.get(ente=self.ente)
        except:
            return None


def data():
    for d in DependienteSepelio.objects.all():
        if d.nombre:
            if len(d.nombre.replace(' ', '')) == 0:
                d.nombre = None
                d.save()

    titular = None
    for x in DependienteSepelio.objects.all().order_by('id'):
        if x.nombre:
            print(x.nombre)
        else:
            print('sin nombre')
        if x.nombre and x.titular:
            titular = x.titular
        if x.nombre and not x.titular:
            titular = None
        if not x.nombre:
            x.titular = titular
            x.save()


def migrar():
    for s in Sepelio.objects.filter(empleado__isnull=False):
        s.cedula = s.empleado.cedula
        s.save()
    for d in DependienteSepelio.objects.filter(titular__isnull=False).order_by('id'):
        s = Sepelio()
        s.empleado = d.titular.empleado
        s.asegurado = d.nombre_dependiente
        s.parentesco = d.parentesco
        s.cedula = d.cedula
        s.save()
