#!/bin/bash

cd /var/app
export PYTHONPATH=/var/app;$PYTHONPATH

git clone git@github.com:divio/django-cms-divio-quickstart.git
cd django-cms-divio-quickstart
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose up
open http://127.0.0.1:8000

DJANGO_SUPERUSER_USERNAME=testuser \
DJANGO_SUPERUSER_PASSWORD=testpass \
python manage.py createsuperuser --noinput

python manage.py migrate --noinput
python manage.py initadmin
python manage.py runserver 0.0.0.0:8080



//docker 
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 8080:15672 rabbitmq:3-management
docker run --name some-redis -p 6379:6379 -d redis


