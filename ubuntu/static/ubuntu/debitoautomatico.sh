
#!/bin/bash
set -e
cd /var/www/webtrust
. ../../../venv/bin/activate
exec python manage.py notificar
