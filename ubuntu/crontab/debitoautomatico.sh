#!/bin/bash
set -e
cd ../..
. venv/bin/activate
exec python manage.py notificar
