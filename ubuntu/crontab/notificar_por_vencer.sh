#!/bin/bash
SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin
set -e
cd ../..
. venv/bin/activate
exec python manage.py notificar_por_vencer
