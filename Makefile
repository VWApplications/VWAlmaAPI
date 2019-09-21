# File Name: Makefile
# Purpose  : Symplify project commands
# Author   : Victor Arnaud
# Date     : 05/08/2019

# Execute some targets in django.mk file with command $ make
all: migrations migrate

# Phone target are used when target not be a file
# If we have a file with same name of target, the
# command will run the same way.
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