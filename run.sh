#!/bin/bash

echo "Run migrations..."
alembic upgrade head

echo "Start app.."
python3 -m app.api
