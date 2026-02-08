#!/usr/bin/env python3
"""
Debug script to test database connection and identify the operational error.
"""
import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from settings import settings
from sqlmodel import SQLModel
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, DatabaseError
import traceback

def test_sync_connection():
    """Test synchronous database connection"""
    print("Testing synchronous database connection...")

    # Validate DATABASE_URL
    if not (settings.DATABASE_URL.startswith("postgresql://") or
            settings.DATABASE_URL.startswith("postgresql+psycopg://") or
            settings.DATABASE_URL.startswith("sqlite:///")):
        raise ValueError(f"DATABASE_URL must be a PostgreSQL or SQLite URL. Got: {settings.DATABASE_URL[:50]}...")

    # Log database URL for debugging (with credentials redacted)
    db_url = settings.DATABASE_URL
    safe_db_url = db_url
    if '@' in db_url:
        try:
            protocol_host_part = db_url.split('@')[0]
            host_db_part = db_url.split('@')[1]
            if '//' in protocol_host_part:
                safe_protocol = protocol_host_part.split('//')[0] + '//'
                safe_db_url = f"{safe_protocol}[REDACTED]@[{host_db_part}]"
        except:
            safe_db_url = "[REDACTED]"

    print(f"Attempting to connect to: {safe_db_url}")

    # Create synchronous engine with enhanced error reporting
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            echo=True,  # Enable to see the actual SQL being executed
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,  # Reduced for debugging
            max_overflow=10,
            pool_timeout=30,
            connect_args={
                "sslmode": "require"
            }
        )

        print("Engine created successfully. Testing connection...")

        # Test basic connection
        with engine.connect() as conn:
            print("+ Connection established")

            # Test basic query
            result = conn.execute(text("SELECT 1 as test;"))
            test_value = result.scalar()
            print(f"+ Basic query successful: {test_value}")

            # Get database info
            result = conn.execute(text("SELECT current_database();"))
            current_db = result.scalar()
            print(f"+ Connected to database: {current_db}")

            # Get server version
            result = conn.execute(text("SHOW server_version;"))
            version = result.scalar()
            print(f"+ Server version: {version}")

        # Inspect database schema
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"+ Tables in database: {tables}")

        # Check for expected tables
        expected_tables = ['user', 'task']
        for table in expected_tables:
            if table in tables:
                print(f"+ Table '{table}' exists")
            else:
                print(f"- Table '{table}' does not exist")

        print("\n=== Synchronous connection test PASSED ===")
        return True

    except OperationalError as e:
        print(f"\n- OperationalError: {str(e)}")
        print("This suggests a connection issue or invalid credentials")
        return False
    except DatabaseError as e:
        print(f"\n- DatabaseError: {str(e)}")
        print("This suggests a database-level issue")
        return False
    except Exception as e:
        print(f"\n- Unexpected error: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False

def test_async_compatibility():
    """Test if there's an async/sync mismatch"""
    print("\nChecking for async/sync driver mismatch...")

    # Check if the URL contains async driver
    if "asyncpg" in settings.DATABASE_URL:
        print("- DATABASE_URL contains 'asyncpg' which suggests async usage")
        print("  But the engine is created synchronously - this is a mismatch!")
        return False
    else:
        print("+ No async driver detected in DATABASE_URL")
        return True

def check_requirements():
    """Check if proper drivers are installed"""
    print("\nChecking installed database drivers...")

    try:
        import psycopg2
        print("+ psycopg2 is available")
    except ImportError:
        print("- psycopg2 is not available")

    try:
        import asyncpg
        print("+ asyncpg is available")
    except ImportError:
        print("i  asyncpg is not available (this is expected for sync connections)")

def main():
    print("=" * 60)
    print("DATABASE CONNECTION DEBUGGER")
    print("=" * 60)

    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")

    # Check for async/sync mismatch first
    async_ok = test_async_compatibility()

    # Check requirements
    check_requirements()

    # Test the connection
    sync_ok = test_sync_connection()

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Async/Sync compatibility: {'+' if async_ok else '-'}")
    print(f"  Synchronous connection: {'+' if sync_ok else '-'}")

    if not sync_ok:
        print("\nPOTENTIAL ISSUES:")
        print("1. Invalid DATABASE_URL credentials")
        print("2. Network connectivity issue")
        print("3. Firewall blocking connection")
        print("4. Database server down")
        print("5. SSL configuration issue")

        if not async_ok:
            print("6. Async/sync driver mismatch")

    print("=" * 60)

if __name__ == "__main__":
    main()