from adminlte.widgets import *
from backend.models import Cliente, Linea, OportunityStatus, Prospect, TagSeguimiento
from django.forms import TextInput


class JsonWidget(Widget):
    template_name = 'trustseguros/lte/widgets/json_form.html'

    def format_value(self, value):
        return value


class CamposAdicionalesWidget(Widget):
    template_name = 'trustseguros/lte/widgets/campos-adicionales.html'

    def format_value(self, value):
        return value


class CoberturasWidget(Widget):
    template_name = "trustseguros/lte/widgets/coberturas.html"

    def format_value(self, value):
        return value


class TablaPagosWidget(Widget):
    template_name = "trustseguros/lte/widgets/tabla-pagos.html"

    def format_value(self, value):
        return value


class CobranzaWidget(Widget):
    template_name = "trustseguros/lte/widgets/cobranza.html"

    def format_value(self, value):
        return value


class PagosWidget(Widget):
    template_name = "trustseguros/lte/widgets/pagos.html"

    def format_value(self, value):
        return [self.attrs['form'](instance=x) for x in value]


class RepresentanteLegalWidget(Widget):
    template_name = "trustseguros/lte/widgets/representante-legal.html"

    def format_value(self, value):
        try:
            return self.attrs['form'](instance=Cliente.objects.get(id=value))
        except:
            return self.attrs['form']


class DriveWidget(Widget):
    template_name = "trustseguros/lte/widgets/drive.html"

    def format_value(self, value):
        return value


class DriveClienteWidget(Widget):
    template_name = "trustseguros/lte/widgets/drive-cliente.html"

    def format_value(self, value):
        if value:
            return [self.attrs['form'](instance=x) for x in value]
        return []


class BitacoraWidget(Widget):
    template_name = "trustseguros/lte/widgets/bitacora.html"

    def format_value(self, value):
        return value


class BitacoraOportunidadWidget(Widget):
    template_name = "trustseguros/lte/widgets/bitacora.oportunidad.html"

    def format_value(self, value):
        return value

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs = {'tags': TagSeguimiento.objects.filter(active=True)}
        return super().build_attrs(base_attrs, extra_attrs)


class PedirComentarioWidget(Widget):
    template_name = "trustseguros/lte/widgets/pedir-comentarios.html"

    def format_value(self, value):
        return value


class ReadOnlyWidget(TextInput):

    def format_value(self, value):
        try:
            return value.name
        except:
            return "VACIO"

    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs['readonly'] = 'readonly'
        return super().build_attrs(base_attrs, extra_attrs)


class FieldMapWidget(Widget):
    template_name = "trustseguros/lte/widgets/field-map.html"

    def format_value(self, value):
        if value:
            return [self.attrs['form'](instance=instance) for instance in
                    value.fieldmap.filter(fieldmap_type=self.attrs['type'])]
        return value


class LineaWidget(Widget):
    template_name = "trustseguros/lte/widgets/linea.html"

    def format_value(self, value):
        return value

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs = {'choices': Linea.objects.all()}
        return super().build_attrs(base_attrs, extra_attrs)


class OportunityStatusWidget(Widget):
    template_name = "trustseguros/lte/widgets/oportunidad-status.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs = {
            'choices': OportunityStatus.choices()
        }
        return super().build_attrs(base_attrs, extra_attrs)


class FormWidget(Widget):
    template_name = "trustseguros/lte/widgets/form-field.html"

    def format_value(self, value):
        try:
            model = self.attrs['form']._meta.model
            instance = model.objects.get(pk=value)
            return self.attrs['form'](instance=instance)
        except:
            return self.attrs['form']


class CotizacionWidget(Widget):
    template_name = "trustseguros/lte/widgets/cotizacion.html"

    def format_value(self, value):
        return value


class CoberturaSubRamoWidget(Widget):
    template_name = "trustseguros/lte/widgets/sub-ramo-coberturas.html"

    def format_value(self, value):
        if value:
            return [self.attrs['form'](instance=x) for x in value]
        return value


class RecibosPrima(Widget):
    template_name = "trustseguros/lte/widgets/recibos-prima.html"

    def format_value(self, value):
        return value


class TramitesSiniestro(Widget):
    template_name = "trustseguros/lte/widgets/tramites-siniestros.html"

    def format_value(self, value):
        return value


class ProspectFormWidget(Widget):
    template_name = "trustseguros/lte/widgets/prospect-form.html"

    def format_value(self, value):
        if value:
            prospect = Prospect.objects.get(id=value)
            return self.attrs['form'](instance=prospect)
        else:
            return self.attrs['form']()
