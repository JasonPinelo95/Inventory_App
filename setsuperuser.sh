#!/bin/bash
# Automatin migration and set of superuser

python manage.py migrate

python manage.py ensure-adminuser.py --user=master --password=theoneaboveall

python manage.py runserver 0.0.0.0:8000
