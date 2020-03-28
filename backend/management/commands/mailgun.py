from django.core.management.base import BaseCommand
from utils.utils import send_simple_message


class Command(BaseCommand):
    help = 'Notificacion polizas a vencer'

    def add_arguments(self, parser):
        parser.add_argument('address', nargs='+', type=str)

    def handle(self, *args, **options):
        send_simple_message(options['address'])





