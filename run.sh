#!/bin/bash

# Production startup script for EC2
export FLASK_APP=app.py
export FLASK_ENV=production

# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 wsgi:app