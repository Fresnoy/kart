#!/bin/sh

echo "⏳ Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL is available - running migrations"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"

