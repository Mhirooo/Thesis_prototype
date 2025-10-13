#!/bin/bash
cd Hirely
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 run:app