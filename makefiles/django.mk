# SERVER -------------------------------------------------------

SERVER = 0.0.0.0:8080

run: project/manage.py
	# Run the development server
	python3 project/manage.py runserver ${SERVER}

# DATABASE -----------------------------------------------------

migrations: project/manage.py
	# Create all migrations from models
	python3 project/manage.py makemigrations

migrate: project/manage.py
	# Migrate all migrations on database
	python3 project/manage.py migrate

superuser: project/manage.py
	# Create a super user on system.
	python3 project/manage.py createsuperuser

sql: project/manage.py
	# Show SQL commands
	python3 project/manage.py sqlmigrate ${app_label} ${migration_name}

# TRANSLATION --------------------------------------------------

files := "project/*.py"

messages:
	# Create a django.po to insert translations (pt-BR)
	django-admin makemessages -l pt_BR -i ${files}

compilemessages:
	# Create translations
	django-admin compilemessages

# STATIC FILES -------------------------------------------------

staticfiles: project/manage.py
	# Collect all static files
	python3 project/manage.py collectstatic --noinput

# POPULATE DB --------------------------------------------------

json := database.json

fixture: project/manage.py
	# Create files with data
	python3 project/manage.py dumpdata ${model} --indent 4 > ${json}

populate: project/manage.py
	# Populate database with specific model
	python3 project/manage.py loaddata project/**/fixtures/**.json