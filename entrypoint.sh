#!/bin/sh
service postgresql start
service redis-server start
cd /hide && sanic app.app:app --host=0.0.0.0 --port=80 --fast
