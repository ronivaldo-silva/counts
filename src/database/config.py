import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Default to Counts Postgres DB
# For Postgres, use: postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://userapp:Li0nt0g3ro!@localhost:5432/Counts")

# Fix for Render/Heroku typically using 'postgres://' which SQLAlchemy doesn't like anymore
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True
)
# Note: check_same_thread=False is needed for SQLite + Multithreading (Flet often runs in threads)
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
