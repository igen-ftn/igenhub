#!/bin/bash
touch docker-compose.yml
echo "version: '2'" > docker-compose.yml
echo "services:" >> docker-compose.yml
echo "    db:"  >> docker-compose.yml
echo "        image: postgres" >> docker-compose.yml
echo "        command: -p 8022" >> docker-compose.yml
echo "        volumes:" >> docker-compose.yml
echo "            - ./postgres-data:/var/lib/postgresql/data" >> docker-compose.yml
echo "    web:" >> docker-compose.yml
echo "        image: kimnovak/igenhub:latest" >> docker-compose.yml
echo "        environment:" >> docker-compose.yml
echo "            - HTTP_PROXY=proxy.uns.ac.rs:8080" >> docker-compose.yml
echo "            - HTTPS_PROXY=proxy.uns.ac.rs:8080" >> docker-compose.yml
echo "        volumes:" >> docker-compose.yml
echo "            - ./media:/code/igenapp/media" >> docker-compose.yml
echo "        ports:" >> docker-compose.yml
echo "            - \"8021:8021\"" >>docker-compose.yml
echo "        depends_on:" >> docker-compose.yml
echo "            - db" >> docker-compose.yml
docker-compose down
docker-compose pull
docker-compose build
docker-compose up -d
docker-compose down
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up -d
