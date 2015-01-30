#!/bin/bash
set -e
python manage.py migrate --noinput
python manage.py test welree 2>&1
