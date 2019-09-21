# DATABASE -----------------------------------------------------

migrations:
	# Create all migrations from models
	docker-compose exec alma python3 manage.py makemigrations

migrate:
	# Migrate all migrations on database
	docker-compose exec alma python3 manage.py migrate

shell:
	# Run django shell
	docker-compose exec alma python3 manage.py shell

superuser:
	# Create a super user on system.
	docker-compose exec alma python3 manage.py createsuperuser

install:
	# Install some dependecy
	docker-compose exec alma pip3 install ${package}

requirements:
	# Verify all requirements
	docker-compose exec alma pip3 freeze

flake8:
	# Run flake8
	docker-compose exec alma flake8

# POPULATE DB --------------------------------------------------

json_file := database.json

fixture:
	# Create files with data
	docker-compose exec alma python3 manage.py dumpdata ${model} --indent 4 > ${json_file}

populate:
	# Populate database with specific model
	docker-compose exec alma python3 manage.py loaddata project/**/fixtures/**.json


# BACKUP e RESTORE

dump:
	# Fazer um backup do banco de dados
	docker-compose exec postgres pg_dump -h localhost -p 5432 -U alma -F c -b -v -f backup/db.backup alma_db

psql:
	# Entrar no banco de dados postgres
	docker-compose exec postgres psql -U alma -d alma_db

drop:
	# Remove o banco de dados para ativar a restauração
	docker-compose exec postgres dropdb -U alma alma_db

restore:
	# Restaurar o banco de dados
	docker-compose exec postgres pg_restore -h localhost -p 5432 -U alma --create --dbname=postgres --verbose backup/db.backup


# RUN TESTS ------------------------------------------------------

path := .

test:
	# Run all tests
	docker-compose exec alma python3 manage.py test ${path} --keepdb