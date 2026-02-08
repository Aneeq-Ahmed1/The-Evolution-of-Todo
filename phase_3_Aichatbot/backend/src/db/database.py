"""
Database connection and initialization for the AI Agent Platform
"""
from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import Pool
from typing import Generator
import os
from .settings import settings
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.agent_session import AgentSession
from ..models.skill_log import SkillExecutionLog


# Validate DATABASE_URL is PostgreSQL before creating engine
if not (settings.database_url.startswith("postgresql://") or
        settings.database_url.startswith("postgresql+psycopg://")):
    raise ValueError(f"DATABASE_URL must be a PostgreSQL URL. Got: {settings.database_url[:50]}...")

# Create the engine with PostgreSQL-specific settings
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL statements in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
    pool_size=20,         # Number of connection objects to keep in the pool
    max_overflow=30,      # Number of connections that can be created beyond pool_size
    pool_timeout=30,      # Number of seconds to wait before giving up on getting a connection
    connect_args={
        "sslmode": "require"  # Ensure SSL is used for Neon connections
    }
)


def init_db():
    """Initialize the database by creating all tables."""
    # Import all models here to ensure they're registered with SQLModel
    # This creates the tables based on the model definitions

    # Create all tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session


# Optional: Add connection pooling event listeners for monitoring
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite-specific pragmas if using SQLite (for local development)."""
    if 'sqlite' in engine.url.drivername:
        cursor = dbapi_connection.cursor()
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()