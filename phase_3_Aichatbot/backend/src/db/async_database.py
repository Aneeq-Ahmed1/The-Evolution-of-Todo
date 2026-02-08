"""
Async database connection and initialization for the AI Agent Platform
"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from typing import AsyncGenerator
import os
from .settings import settings


# Validate DATABASE_URL is PostgreSQL before creating engine
if not (settings.database_url.startswith("postgresql://") or
        settings.database_url.startswith("postgresql+psycopg://")):
    raise ValueError(f"DATABASE_URL must be a PostgreSQL URL. Got: {settings.database_url[:50]}...")

# Create the async engine - use asyncpg for PostgreSQL
async_database_url = settings.database_url
if async_database_url.startswith("postgresql://"):
    # Replace with async PostgreSQL driver
    async_database_url = async_database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove sslmode and channel_binding from URL since asyncpg handles SSL automatically
if "?" in async_database_url:
    # Extract parameters and rebuild URL without problematic parameters
    from urllib.parse import urlparse, parse_qs, urlencode
    parsed = urlparse(async_database_url)
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    
    # Remove problematic parameters from query parameters
    params_to_remove = ['sslmode', 'channel_binding']
    for param in params_to_remove:
        if param in query_params:
            del query_params[param]
    
    # Reconstruct the URL without problematic parameters
    new_query = urlencode(query_params, doseq=True)
    async_database_url = parsed._replace(query=new_query).geturl()

# Configure SSL context for asyncpg connections to Neon
connect_args = {
    "server_settings": {
        "application_name": "ai_agent_platform",
    }
}

async_engine = create_async_engine(
    async_database_url,
    echo=settings.debug,  # Log SQL statements in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
    pool_size=20,         # Number of connection objects to keep in the pool
    max_overflow=30,      # Number of connections that can be created beyond pool_size
    pool_timeout=30,      # Number of seconds to wait before giving up on getting a connection
    connect_args=connect_args,
)


async def init_db():
    """Initialize the database by creating all tables."""
    # Import all models here to ensure they're registered with SQLModel
    # This creates the tables based on the model definitions
    from sqlmodel import SQLModel

    async with async_engine.begin() as conn:
        # Create all tables - this requires async execution
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session."""
    async with AsyncSession(async_engine) as session:
        yield session