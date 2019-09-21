# DOCKER DEPLOY ------------------------------------------------
up:
	# Create and start containers
	docker-compose up

build:
	# Rebuild the docker compose
	docker-compose up --build

restart:
	# Restart services
	docker-compose restart

logs:
	# View output from containers
	docker-compose logs -f -t

start:
	# Start services
	docker-compose start

stop:
	# Stop services
	docker-compose stop

ps:
	# List all running containers
	docker-compose ps

ps_all:
	# List all containers
	docker ps -a

down:
	# Stop and Remove all containers
	docker-compose down

help:
	# Help of docker-compose commands
	docker-compose help

images:
	# List images
	docker images

container := "alma"

exec:
	# Get in the bash of container
	docker-compose exec ${container} bash