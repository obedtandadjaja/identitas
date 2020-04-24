#! /usr/bin/env bash
set -e

python /app/celeryworker_prestart.py

celery worker -A app.worker -l info -Q main-queue -c 1
