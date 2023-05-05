#!/bin/bash

# run celerybeat
python3 -m celery -A src.celery:celery_app beat --loglevel=INFO &

# run celery workers
python3 -m celery -A src.celery:celery_app worker --loglevel=INFO &

sleep 20 # wait for celery to start
# run receiver
echo "Starting the receiver"
python3 -u src/receiver.py