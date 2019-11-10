#!/bin/bash
#
# Propósito: Configura o ambiente de produção
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Inicializando o celery"
[ -e celeryd.pid ] && rm celeryd.pid
celery -A vwa worker -l info -f vwa/celery.logs -D

echo "Inicializando o celery-beat"
[ -e celerybeat.pid ] && rm celerybeat.pid
celery -A vwa beat -l info -f vwa/celery-beat.logs --detach

# Espera o POSTGRESQL inicializar
postgres_ready() {
python3 << END
import sys
import psycopg2
import os
try:
    psycopg2.connect(
      dbname=os.environ.get("POSTGRES_DB", "vwapp_db"),
      user=os.environ.get("POSTGRES_USER", "vwapp"),
      password=os.environ.get("POSTGRES_PASSWORD", "vwapp"),
      host=os.environ.get("POSTGRES_HOST", "postgres")
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgresql is unavailable - Waiting..."
  sleep 1
done

echo "Creating migrations and insert into psql database"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Run server"
gunicorn vwa.wsgi --bind 0.0.0.0:8000 --reload --graceful-timeout=900 --timeout=900 --log-level DEBUG --workers 5