# DATABASE -----------------------------------------------------

migrations:
	# Cria todas as migrações
	docker-compose exec vwapp python3 manage.py makemigrations

migrate:
	# Rodas as migrações no banco de dados
	docker-compose exec vwapp python3 manage.py migrate

shell:
	# Roda o shell do django
	docker-compose exec vwapp python3 manage.py shell

superuser:
	# Cria um superusuário
	docker-compose exec vwapp python3 manage.py createsuperuser

install:
	# Instala uma nova dependência
	docker-compose exec vwapp pip3 install ${package}

remove:
	# Remove um pacote
	docker-compose exec vwapp pip3 uninstall ${package}

requirements:
	# Verifica todas as dependências
	docker-compose exec vwapp pip3 freeze > project/requirements.txt

flake8:
	# Roda o flake8
	docker-compose exec vwapp flake8

# POPULATE DB --------------------------------------------------

json_file := database.json

fixture:
	# Cria um arquivo json com os dados do banco.
	docker-compose exec vwapp python3 manage.py dumpdata ${model} --indent 4 > ${json_file}

populate:
	# Popula o banco de dados com esse arquivo json gerado.
	docker-compose exec vwapp python3 manage.py loaddata project/**/fixtures/**.json


# BACKUP e RESTORE

dump:
	# Fazer um backup do banco de dados
	docker-compose exec postgres pg_dump -h localhost -p 5432 -U vwapp -F c -b -v -f backup/db.backup vwapp_db

psql:
	# Entrar no banco de dados postgres
	docker-compose exec postgres psql -U vwapp -d vwapp_db

drop:
	# Remove o banco de dados para ativar a restauração
	docker-compose exec postgres dropdb -U vwapp vwapp_db

restore:
	# Restaurar o banco de dados
	docker-compose exec postgres pg_restore -h localhost -p 5432 -U vwapp --create --dbname=postgres --verbose backup/db.backup


# RUN TESTS ------------------------------------------------------

path := .

test:
	# Roda todos os testes
	docker-compose exec vwapp python3 manage.py test ${path} --keepdb