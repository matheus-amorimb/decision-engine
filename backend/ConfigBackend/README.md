# Backend

## Overview

Welcome to the **ConfigBackend**, the glorious REST API responsible for managing and executing decision policy flows. Here, you get to play god—defining decision-making policies with configurable rules and conditions that will later be used to compute automated decisions (because who wants humans making decisions anyway?).

## Tech Stack

- **Python** (because we love snake-themed programming languages)
- **FastAPI** (for blazing-fast APIs and async magic)
- **SQLAlchemy** (because writing raw SQL is for the brave)
- **PostgreSQL** (a.k.a. the _chad_ of databases)
- **Pydantic** (so our data models don’t turn into chaos)
- **Alembic** (for when we inevitably need to update the database schema)
- **Pytest** (so we can pretend we write tests)

---

## Installation

It’s kind of obvious, but let’s make it crystal clear: all these commands assume you’re inside the **ConfigBackend/** folder. If you’re reading this from elsewhere... well, now you know where you should be.

### 1. Installing Dependencies

I use **uv** to manage dependencies because it’s cool and fast, but feel free to use whatever package manager your heart desires.

#### Option 1: Using `uv` (recommended because I said so)

```zsh
uv venv # Create the virtual environment

source .venv/bin/activate # Activate the virtual environment

uv pip sync requirements.txt # Install dependencies in the virtual environment
```

#### Option 2: The old-fashioned way

If you’re not into `uv`, install dependencies manually:

```zsh
pip install -r requirements.txt
```

---

### 2. Setting Up the Database

#### 2.1 Installing PostgreSQL

We use **PostgreSQL** as our database. You’ll need an instance of PostgreSQL running on your machine. My strong recommendation? **Use Docker**—because who wants to deal with manual installations in 2025?

#### 2.2 Running PostgreSQL with Docker (Recommended)

A `docker-compose.yaml` file is chilling at the root of this project. Just run:

```zsh
docker-compose up -d
```

Boom. Instant PostgreSQL setup.

#### 2.3 Configuring the Database Connection

Once your PostgreSQL instance is up, you need to tell the project where to find it. Open the `.env` file and update the connection details:

```.env
DATABASE_URL="postgresql+asyncpg://<user>:<password>@localhost:<port>/<database_name>"
```

If you used the `docker-compose.yaml` file, **you can skip this step**. The defaults should work just fine.

#### 2.4 Running Migrations

Now that your database is up and configured, let's use **Alembic** to create the tables:

```zsh
# Generate a new migration file
alembic revision --autogenerate -m "initial migration"

# Apply the migration to the database
alembic upgrade head
```

#### The Life-Saving Shortcut™

If you don’t want to run all these commands every time you restart your Docker container, just use the **`init_db.sh`** script inside the `scripts/` folder. This script:

- Starts your database container
- Runs migrations
- **Populates your database** using `src/seed.py`

Ain’t nobody got time for manual setups.

---

## Running the Project (Finally)

Before launching the API, we need to make sure Python knows where our `src` folder is. Otherwise, it might throw a tantrum.

- **Linux/macOS:**

```zsh
export PYTHONPATH=$PYTHONPATH:"$PWD"
```

- **Windows (I forgive you for using it):**

```powershell
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"
```

With everything set up, it’s time to **run the API**:

```zsh
fastapi dev src/app.py
```

Your application should now be available at:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)** 🎉

---

## Documentation

Want to see all the endpoints and how to use them? Head over to the **Swagger documentation**:

📜 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

It’s all there: endpoints, request/response schemas, and even a fancy UI to test your API.

---

I hope you enjoy this project as much as I enjoyed making it! 🚀
