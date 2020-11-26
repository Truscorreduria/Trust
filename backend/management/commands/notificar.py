from django.core.management.base import BaseCommand
from backend.cron import *


class Command(BaseCommand):
    help = 'Notificación de pólizas a vencer'

    def handle(self, *args, **options):
        notificacion_pagos_vencidos()
