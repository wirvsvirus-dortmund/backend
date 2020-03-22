#! /bin/sh

set -e

# first backup!
pg_dump $DATABASE_URI > /var/backups/$(date +"%Y-%m-%dT%H%M%S").sql

# apply database migrations
flask db upgrade

# start the server
gunicorn --bind 0.0.0.0:$PORT "backend:create_app()"
