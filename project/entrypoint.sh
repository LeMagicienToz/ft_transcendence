#!/bin/sh

# Run database migrations
python manage.py migrate

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 ft_transcendence.wsgi:application
