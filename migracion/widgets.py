from django.forms import Widget


class Automoviles(Widget):
    template_name = 'migracion/widgets/automoviles.html'

    def format_value(self, value):
        return value


class Accidentes(Widget):
    template_name = 'migracion/widgets/accidentes.html'

    def format_value(self, value):
        return value


class Sepelios(Widget):
    template_name = 'migracion/widgets/sepelios.html'

    def format_value(self, value):
        return value