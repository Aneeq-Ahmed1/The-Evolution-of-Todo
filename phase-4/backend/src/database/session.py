from sqlmodel import create_engine, Session
from sqlalchemy import URL
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    """
    Get a database session.
    """
    with Session(engine) as session:
        yield session