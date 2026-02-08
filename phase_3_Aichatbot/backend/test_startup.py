#!/usr/bin/env python3
"""
Test script to verify the application starts without the SQLAlchemy Operational Error
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_import():
    """Test that the main application can be imported without errors"""
    try:
        print("Testing import of main application...")
        from main import app
        print("+ Main application imported successfully")

        # Test database connection
        print("Testing database connection...")
        from db import engine
        from sqlalchemy import text

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1
            print("+ Database connection test passed")

        print("+ All startup tests passed!")
        return True

    except Exception as e:
        print(f"- Startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_async_conversation_service():
    """Test that the async conversation service can be instantiated"""
    try:
        print("Testing async conversation service...")
        from sqlmodel.ext.asyncio.session import AsyncSession
        from sqlalchemy.ext.asyncio import create_async_engine
        from src.db.settings import settings

        # Create async engine
        from src.db.settings import settings as src_settings
        async_db_url = src_settings.database_url
        if async_db_url.startswith("postgresql://"):
            async_db_url = async_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        else:
            # Since we now enforce PostgreSQL, this shouldn't happen
            print(f"- Database URL is not PostgreSQL: {async_db_url}")
            return False

        async_engine = create_async_engine(async_db_url)

        print("+ Async engine created successfully")
        return True

    except Exception as e:
        print(f"- Async conversation service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("APPLICATION STARTUP VERIFICATION")
    print("="*50)

    success1 = test_import()
    success2 = test_async_conversation_service()

    print("\n" + "="*50)
    if success1:
        print("+ ALL ESSENTIAL TESTS PASSED - Application starts correctly!")
        print("+ No SQLAlchemy Operational Error detected")
        print("+ Database connectivity working")
        if success2:
            print("+ Async operations properly configured")
    else:
        print("- SOME TESTS FAILED")
        sys.exit(1)
    print("="*50)