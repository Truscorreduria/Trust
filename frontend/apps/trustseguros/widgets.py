from adminlte.widgets import *
from backend.models import Cliente


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


class BitacoraWidget(Widget):
    template_name = "trustseguros/lte/widgets/bitacora.html"

    def format_value(self, value):
        return value
