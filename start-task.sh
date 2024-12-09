#! /bin/bash

venv/bin/celery -A settings worker -P threads -c 5 -l info -n dashboard@%h
