#!/bin/bash
# Render startup script - forces correct gunicorn command
echo "Starting Hirely with wsgi:app entry point..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 wsgi:app