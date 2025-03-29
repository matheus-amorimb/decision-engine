#!/bin/bash

set -e

echo "Current working directory: $(pwd)"

echo "Stopping and removing containers..."
docker-compose down

echo "Starting Docker containers..."
docker-compose up -d

echo "Waiting for the database to be ready"
sleep 10

echo "Removing old migration versions..."
rm -rf migration/versions/*  

echo "Running initial migrations..."
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

echo "Adding the src directory to the Python path for proper module imports..."
export PYTHONPATH=$PYTHONPATH:"$PWD"

echo "Seeding the database..."
python src/seed.py

echo "Database initialization complete!"
