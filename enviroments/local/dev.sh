#!/bin/bash
#
# Purpose: Config development enviroment
#
# Author: Victor Arnaud <victorhad@gmail.com>

echo "Creating migrations and insert into sqlite database"
make makemigrations
make migrate

echo "Run the server"
make run