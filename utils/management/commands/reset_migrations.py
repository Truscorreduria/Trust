from django.core.management.base import BaseCommand
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Reset migrations'

    apps = ['cotizador', 'utils']

    def handle(self, *args, **options):
        for app in self.apps:

            os.system("rm %s/*.*" % (
                os.path.join(settings.BASE_DIR, app, 'migrations'))
                      )

            os.system("touch %s/__init__.py" % (
                os.path.join(settings.BASE_DIR, app, 'migrations'))
                      )





