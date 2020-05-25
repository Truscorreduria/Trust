#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/var/www/webtrust/ubuntu/crontab
set -e
cd ../..
. venv/bin/activate
exec python manage.py notificar_por_vencer
