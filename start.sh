#!/bin/sh
set -e

# Startup script for Sevalla deployment
# - Runs migrations and collectstatic at runtime
# - Starts gunicorn on PORT assigned by platform

echo "Starting startup script..."
echo "Using Python: $(python --version 2>/dev/null || echo 'unknown')"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Use PORT env var if provided, otherwise default to 8080
PORT=${PORT:-8080}

echo "Starting gunicorn on port $PORT..."
exec gunicorn countries_project.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 2

