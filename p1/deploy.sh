#!/bin/bash

cd /home/ubuntu/myprojectenv

# Activate virtual environment
source myprojectenv/bin/activate

cd deployment/

# Install dependencies
pip install -r requirement.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn
sudo systemctl restart gunicorn.service nginx.service