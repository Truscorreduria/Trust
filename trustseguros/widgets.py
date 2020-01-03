from django.forms import Widget, Select
from .models import Cliente


# region admin

class formaPago(Widget):
    template_name = 'trustseguros/widgets/forma_pago.html'

    def format_value(self, value):
        return value


class listaPolizas(Widget):
    template_name = 'trustseguros/widgets/lista_polizas.html'

    def format_value(self, value):
        return value


class listaEndosos(Widget):
    template_name = 'trustseguros/widgets/lista_endosos.html'

    def format_value(self, value):
        return value


class polizasGrupo(Widget):
    template_name = 'trustseguros/widgets/polizas_grupo.html'

    def format_value(self, value):
        return value


class autoCompleteCliente(Widget):
    template_name = 'trustseguros/widgets/autocomplete_cliente.html'

    def format_value(self, value):
        try:
            return Cliente.objects.get(id=value).to_json()
        except:
            return None


# endregion


# region lte
class SelectSearch(Select):
    template_name = "trustseguros/lte/widgets/select-search.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs.update({
            'class': "selectpicker",
            'data-live-search': "true"
        })
        return super().build_attrs(base_attrs, extra_attrs=extra_attrs)

# endregion
