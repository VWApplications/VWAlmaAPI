#!/usr/bin/env bash
# Continuos deploy
git fetch origin
echo y | sudo docker-compose -f docker-compose.deploy.yml rm --stop vwa-nginx
echo y | sudo docker-compose -f docker-compose.deploy.yml rm --stop vwa
git pull origin master
sudo docker-compose -f docker-compose.deploy.yml up -d --build