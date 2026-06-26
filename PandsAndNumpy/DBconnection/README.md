# Pandas & PostgreSQL Connection

This project demonstrates how to connect Pandas to a PostgreSQL database running in Docker using SQLAlchemy and psycopg2.

## Prerequisites

- Python 3.13
- Pandas
- SQLAlchemy
- psycopg2-binary
- Docker
- PostgreSQL

Install the required packages:

```bash
pip install pandas sqlalchemy psycopg2-binary
```

## Start PostgreSQL

Run the Docker containers:

```bash
docker compose up -d
```

## Database Configuration

| Property | Value |
|----------|-------|
| Database | `mydb` |
| Username | `admin` |
| Password | `secret123` |
| Host | `localhost` |
| Port | `5432` |

## Create Database Engine

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://admin:secret123@localhost:5432/mydb"
)
```

## Connection String Format

```text
postgresql+psycopg2://username:password@host:port/database
```