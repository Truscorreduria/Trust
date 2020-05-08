from django.core.management.base import BaseCommand
from frontend.apps.cotizador.views import iniciar_proc


class Command(BaseCommand):
    help = 'Autorenovacion automatica de polizas del cotizador'

    def handle(self, *args, **options):
        iniciar_proc()





