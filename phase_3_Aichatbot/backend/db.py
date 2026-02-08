from sqlmodel import create_engine, Session
from typing import Generator
from settings import settings
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# Validate DATABASE_URL is either PostgreSQL or SQLite (allow SQLite for development)
if not (settings.DATABASE_URL.startswith("postgresql://") or
        settings.DATABASE_URL.startswith("postgresql+psycopg://") or
        settings.DATABASE_URL.startswith("sqlite:///")):
    raise ValueError(f"DATABASE_URL must be a PostgreSQL or SQLite URL. Got: {settings.DATABASE_URL[:50]}...")

# Determine if we're using PostgreSQL or SQLite
if settings.DATABASE_URL.startswith("sqlite:///"):
    # For SQLite, use simpler connection parameters
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,  # Set to True for SQL query logging in development
    )
else:
    # For PostgreSQL (including Neon), use connection pooling parameters
    # Remove sslmode and channel_binding from URL since asyncpg handles SSL automatically
    database_url = settings.DATABASE_URL
    if "?" in database_url:
        # Extract parameters and rebuild URL without problematic parameters
        from urllib.parse import urlparse, parse_qs, urlencode
        parsed = urlparse(database_url)
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        
        # Remove problematic parameters from query parameters
        params_to_remove = ['sslmode', 'channel_binding']
        for param in params_to_remove:
            if param in query_params:
                del query_params[param]
        
        # Reconstruct the URL without problematic parameters
        new_query = urlencode(query_params, doseq=True)
        database_url = parsed._replace(query=new_query).geturl()
    
    engine = create_engine(
        database_url,
        echo=False,  # Set to True for SQL query logging in development
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_size=20,  # Number of connection objects to keep in the pool
        max_overflow=30,  # Number of connections that can be created beyond pool_size
        pool_timeout=30,  # Number of seconds to wait before giving up on getting a connection
        connect_args={}  # Empty connect_args since asyncpg handles SSL automatically
    )

# Safe logging of DATABASE_URL with credentials redacted
safe_db_url = settings.DATABASE_URL
if '@' in settings.DATABASE_URL:
    try:
        # Extract the part before @ (protocol://user:pass) and after @ (host:port/db)
        protocol_host_part = settings.DATABASE_URL.split('@')[0]
        host_db_part = settings.DATABASE_URL.split('@')[1]
        # Redact credentials in the first part
        if '//' in protocol_host_part:
            auth_part = protocol_host_part.split('//')[1]  # Get user:pass part
            safe_protocol = protocol_host_part.split('//')[0] + '//'
            safe_db_url = f"{safe_protocol}[REDACTED]@[{host_db_part}]"
        else:
            safe_db_url = f"[REDACTED]@[{host_db_part}]"
    except:
        safe_db_url = "[REDACTED]"

logger.info(f"Database engine created with URL: {safe_db_url}")
logger.info(f"Database type: PostgreSQL (Neon)")

# Test connection and log database info
try:
    from sqlalchemy import text
    with engine.connect() as conn:
        # Get current database name
        result = conn.execute(text("SELECT current_database();"))
        current_db = result.scalar()
        logger.info(f"Current database: {current_db}")

        # Get current schema
        result = conn.execute(text("SELECT current_schema();"))
        current_schema_name = result.scalar()
        logger.info(f"Current schema: {current_schema_name}")

        # Get Neon branch info if available
        try:
            result = conn.execute(text("SELECT current_setting('neon.branch_name', true);"))
            branch_name = result.scalar()
            if branch_name:
                logger.info(f"Neon branch: {branch_name}")
            else:
                logger.info("Not running on Neon (branch info not available)")
        except:
            logger.info("Not running on Neon or branch info not available")

except Exception as e:
    logger.error(f"Could not fetch database info: {str(e)}")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session