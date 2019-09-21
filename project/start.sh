#!/bin/bash
#
# Purpose: Config production enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

# Waiting the PostgreSQL initialize
postgres_ready() {
python3 << END
import sys
import psycopg2
import os
try:
    psycopg2.connect(
      dbname=os.environ.get("POSTGRES_DB", "alma_db"),
      user=os.environ.get("POSTGRES_USER", "alma"),
      password=os.environ.get("POSTGRES_PASSWORD", "alma"),
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