# DOCKER DEPLOY ------------------------------------------------
up:
	# Cria e inicia os containers
	docker-compose up

build:
	# Reconstroi os containers
	docker-compose up --build

restart:
	# Da um restart no servidor
	docker-compose restart

logs:
	# Visualiza os logs
	docker-compose logs -f -t

start:
	# Inicia um container parado
	docker-compose start

stop:
	# Para um container rodando
	docker-compose stop

ps:
	# Lista todos os containers rodando
	docker-compose ps

ps_all:
	# Lista todos os containers
	docker ps -a

down:
	# Para e remove todos os containers
	docker-compose down

help:
	# Help of docker-compose commands
	docker-compose help

images:
	# Lista todas as imagens
	docker images

container := "alma"

bash:
	# Entra no terminal do container
	docker-compose exec ${container} bash