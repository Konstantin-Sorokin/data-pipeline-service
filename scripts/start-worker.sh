#!/bin/sh
set -e

echo "Starting Celery worker..."

exec celery \
    -A app.celery:celery_app \
    worker \
    --loglevel=info \
    --pool=solo