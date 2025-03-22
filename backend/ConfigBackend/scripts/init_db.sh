#!/bin/bash

set -e

echo "Current working directory: $(pwd)"

echo "Stopping and removing containers..."
docker-compose down

echo "Starting Docker containers..."
docker-compose up -d

echo "Waiting for the database to be ready"
sleep 5

echo "Running initial migrations..."
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

echo "Seeding the database..."
python src/seed.py

echo "Database initialization complete!"
