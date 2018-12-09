#!/bin/bash
#
# Purpose: Config homolog enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Creating migrations and insert into sqlite database"
python3 project/manage.py makemigrations
python3 project/manage.py migrate

echo "Run the server"
python3 project/manage.py runserver