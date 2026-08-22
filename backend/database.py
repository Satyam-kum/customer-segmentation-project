
import os
from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

# Current file:
# backend/database.py
#
# We explicitly load:
# backend/.env
#
# This avoids problems caused by running Uvicorn
# from the project root.

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        f"DATABASE_URL was not found in {ENV_FILE}"
    )


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# BASE MODEL
# ============================================================

Base = declarative_base()


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():
    """
    Create all database tables defined in models.py.

    The models module is imported inside the function to
    avoid circular-import problems.
    """

    from backend import models

    Base.metadata.create_all(
        bind=engine
    )


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    FastAPI database dependency.

    Opens a database session for the request and closes it
    automatically after the request is finished.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# OPTIONAL DATABASE CONNECTION TEST
# ============================================================

def test_database_connection():
    """
    Test whether the application can connect to the database.
    """

    from sqlalchemy import text

    db = SessionLocal()

    try:

        db.execute(
            text("SELECT 1")
        )

        return True

    except Exception as e:

        print(
            f"Database connection failed: {e}"
        )

        return False

    finally:

        db.close()