#!/usr/bin/env sh

set -e

export PGPASSWORD="$DATABASE_PASSWORD"

until psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c '\q' 2>/dev/null; do
  echo "Waiting for PostgreSQL connection to be established..."
  sleep 1
done

exec "$@"
