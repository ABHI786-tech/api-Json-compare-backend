import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_SQL_DATABASE")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL or POSTGRES_SQL_DATABASE environment variable not set")

DATABASE_URL = DATABASE_URL.strip().strip('"').strip("'")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
