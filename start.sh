#!/bin/sh
set -e

# Startup script for Leapcell
# - Writes Aiven CA from SSL_CA_B64 or SSL_CA env var into /app/secrets/aiven-ca.pem
# - Runs migrations and collectstatic at runtime (after secrets are available)
# - Starts gunicorn

echo "Starting startup script..."

# Ensure /app/secrets exists
mkdir -p /app/secrets

# If base64-encoded CA provided, decode it into a file
if [ -n "${SSL_CA_B64:-}" ]; then
  echo "Writing Aiven CA from SSL_CA_B64..."
  echo "$SSL_CA_B64" | base64 -d > /app/secrets/aiven-ca.pem
  chmod 640 /app/secrets/aiven-ca.pem || true
  export SSL_CA_PATH=/app/secrets/aiven-ca.pem
fi

# If raw SSL_CA provided (not base64), write it too
if [ -n "${SSL_CA:-}" ] && [ -z "${SSL_CA_B64:-}" ]; then
  echo "Writing Aiven CA from SSL_CA..."
  printf "%s\n" "$SSL_CA" > /app/secrets/aiven-ca.pem
  chmod 640 /app/secrets/aiven-ca.pem || true
  export SSL_CA_PATH=/app/secrets/aiven-ca.pem
fi

echo "Using Python: $(python --version 2>/dev/null || echo 'unknown')"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn countries_project.wsgi:application --bind 0.0.0.0:8080
