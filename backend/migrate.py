#!/usr/bin/env python

"""
Database migration script for Todo application
This script sets up the initial database schema
"""

import os
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import SQLModel
from phase_2_web.backend import models  # Import all models to register them
from phase_2_web.backend.db import engine  # Import the engine from local db module
from phase_2_web.backend.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_db_and_tables():
    """
    Create database tables with enhanced logging and verification
    """
    logger.info("Starting database table creation...")

    # Log database connection info
    db_url = settings.DATABASE_URL
    safe_db_url = db_url
    if '@' in db_url:
        try:
            protocol_host_part = db_url.split('@')[0]
            host_db_part = db_url.split('@')[1]
            if '//' in protocol_host_part:
                safe_protocol = protocol_host_part.split('//')[0] + '//'
                safe_db_url = f"{safe_protocol}[REDACTED]@[{host_db_part}]"
            else:
                safe_db_url = f"[REDACTED]@[{host_db_part}]"
        except:
            safe_db_url = "[REDACTED]"

    logger.info(f"Connecting to database: {safe_db_url}")

    # Determine database type
    db_type = "unknown"
    if db_url.startswith("postgresql://") or db_url.startswith("postgresql+psycopg://"):
        db_type = "postgresql"
    elif db_url.startswith("sqlite:///"):
        db_type = "sqlite"
    logger.info(f"Database type: {db_type}")

    # Log registered tables
    registered_tables = list(SQLModel.metadata.tables.keys())
    logger.info(f"Registered tables in metadata: {registered_tables}")

    try:
        # Create the tables
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully!")

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Tables found in database after creation: {existing_tables}")

        # Check for expected tables
        expected_user_tables = ['user', 'users']
        expected_task_tables = ['task', 'tasks']

        user_table_found = any(table in existing_tables for table in expected_user_tables)
        task_table_found = any(table in existing_tables for table in expected_task_tables)

        if user_table_found and task_table_found:
            logger.info("✅ SUCCESS: Both user and task tables exist in the database!")
        else:
            logger.warning("⚠️  WARNING: Expected tables not found in the database!")
            logger.info(f"Expected user tables: {expected_user_tables}, found: {user_table_found}")
            logger.info(f"Expected task tables: {expected_task_tables}, found: {task_table_found}")

    except Exception as e:
        logger.error(f"❌ ERROR: Failed to create database tables: {str(e)}")
        raise


if __name__ == "__main__":
    create_db_and_tables()
