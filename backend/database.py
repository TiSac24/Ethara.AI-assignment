from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Database URL - defaults to SQLite for easy setup, can be changed to PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./hrms.db"
)

# For PostgreSQL, use format: "postgresql://user:password@localhost/dbname"
# For SQLite (default), use: "sqlite:///./hrms.db"

# Connection pool settings for production (PostgreSQL)
if "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
    )
else:
    # SQLite configuration (for local development)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

