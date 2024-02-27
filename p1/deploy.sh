#!/bin/bash

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    # If not installed, install nginx
    sudo apt update
    sudo apt install nginx -y
fi

sudo systemctl restart nginx

# Check if virtual environment exists
if [ ! -d "/home/ubuntu/myprojectenv" ]; then
    # If not, create virtual environment
    sudo -H pip3 install virtualenv
    virtualenv /home/ubuntu/myprojectenv
fi

cd /home/ubuntu/
source myprojectenv/bin/activate
cd deployment/
pip install -r requirement.txt