#!/bin/bash
cd home/uksdocker/tim-igen/
touch docker-compose.yml
echo "version: '3'" > docker-compose.yml
echo "services:" >> docker-compose.yml
echo "    db:"  >> docker-compose.yml
echo "      image: postgres" >> docker-compose.yml
echo "      command: -p 8022" >> docker-compose.yml
echo "      volumes:" >> docker-compose.yml
echo "         - ./postgres-data:/var/lib/postgresql/data" >> docker-compose.yml
echo "    web:" >> docker-compose.yml
echo "      image: kimnovak/igenhub:latest" >> docker-compose.yml
echo "      command: python3 manage.py runserver 0.0.0.0:8021" >> docker-compose.yml
echo "      ports:" >> docker-compose.yml
echo "        - \"8021:8021\"" >>docker-compose.yml
echo "      volumes:" >> docker-compose.yml
echo "         - .:/code" >> docker-compose.yml
echo "     depends_on:" >> docker-compose.yml
echo "        - db" >> docker-compose.yml
docker-compose down
docker-compose pull
docker-compose up -d