#!/bin/sh
set -e

python -c "from src.db import wait_for_db, init_db; wait_for_db(); init_db()"
exec gunicorn -w 2 -b 0.0.0.0:5000 src.main:app
