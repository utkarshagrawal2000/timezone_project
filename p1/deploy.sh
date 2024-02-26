#!/bin/bash


sudo systemctl restart nginx
cd /home/ubuntu/
source myprojectenv/bin/activate
cd deployment/
pip install -r requirement.txt
