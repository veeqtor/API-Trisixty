#!/usr/bin/env bash

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
BOLD="\e[1m"
DEFAULT="\e[39m"

database_setups(){
    python manage.py wait_for_db
    python manage.py migrate
    python manage.py collectstatic --noinput
    sleep 2
}


API_startup() {

    # Celery
    celery worker -A src.celery --loglevel=info --concurrency=4 &
    sleep 5
    echo  "\n"
    gunicorn --access-logfile '-' \
        --workers 2 --timeout 3600 \
        src.wsgi:application --bind 0.0.0.0:$PORT \
        --access-logformat "%(h)s %(u)s %(t)s '%(r)s' %(s)s '%(f)s' '%(a)s'"
}


main() {

    # Set up the database
    echo "\n"
    echo $YELLOW$BOLD"==========[ Setting up the database. ]=========="
    database_setups
    sleep 2

    # Start server
    echo -e "\n \n"
    echo $GREEN$BOLD"==========[ Starting the server ]=========="
    API_startup
}

main
