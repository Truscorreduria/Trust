from django.core.management.base import BaseCommand
from backend.cron import notificacion_por_vencer_grupo


class Command(BaseCommand):
    help = 'Notificación de pólizas a vencer'

    def handle(self, *args, **options):
        notificacion_por_vencer_grupo()
