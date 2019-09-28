# Nome do arquivo: Makefile
# Propósito  	 : Simplifica e agiliza o desenvolvimento
# Autor   		 : Victor Arnaud
# Data     		 : 05/08/2019

# Ao executar o comando "make" executa make migrations e make migrate ao mesmo tempo
all: migrations migrate

# Phone target é usado quando o target não é um arquivo
# Se você tiver um arquivo com o mesmo nome do target, o
# comando irá rodar da mesma forma.
.PHONE: all

# DJANGO
include makefiles/django.mk

# DOCKER
include makefiles/docker.mk

# SHELL
# make <target>: Execute the commands inside the target
# make -f <filename> <target>: Execute Makefile with another name
# make <target> -n: Show the commands that will be executed by this target
# make <target> -s: Execute the commands without show the commands (silense)