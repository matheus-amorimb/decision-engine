FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Add the application directory to the Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Copy the dependency file into the container
COPY requirements.txt .

# Install necessary system dependencies for PostgreSQL and C extensions
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy all application files into the container
COPY . .

# Run Alembic migrations and start the FastAPI server
CMD alembic revision --autogenerate -m "Initial migration" && alembic upgrade head && fastapi run ./src/app.py --host 0.0.0.0 --port 8000 --reload
