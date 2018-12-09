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
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgresql is unavailable - Waiting..."
  sleep 1
done

echo "Deleting migrations"
find . -path "project/*/migrations/*.pyc"  -delete
find . -path "project/*/migrations/*.py" -not -name "__init__.py" -delete

echo "Deleting staticfiles"
find . -path "project/vwa_accounts/staticfiles/*"  -delete
find . -path "project/vwa_accounts/mediafiles/*"  -delete

echo "Creating migrations and insert into psql database"
python3 project/manage.py makemigrations
python3 project/manage.py migrate
python3 project/manage.py compilemessages
python3 project/manage.py staticfiles

echo "Run server"
gunicorn --bind 0.0.0.0:8000 --chdir project vwa_accounts.wsgi