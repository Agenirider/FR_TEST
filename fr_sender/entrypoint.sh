#!/bin/sh
while ! mysqladmin ping -h"$DB_HOST" --silent;
do
    sleep 1;
done

python manage.py migrate
python manage.py ensure_admin
python manage.py collectstatic --noinput
gunicorn -w 2 -b 0.0.0.0:8000 fr_sender.wsgi --timeout 3600 --workers 4