from django.core.management.base import BaseCommand
from travel_bridge.utils import *


class Command(BaseCommand):
    help = 'Sincronizar base de datos con api de travel banpro'

    def handle(self, *args, **options):
        # fetch_currencies()
        # fetch_category_plan()
        # fetch_territory()
        # fetch_country()
        # fetch_city()
        fetch_plan()