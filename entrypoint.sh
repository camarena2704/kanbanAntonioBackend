#!/bin/sh

echo "Waiting for PostgreSQL service..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"
