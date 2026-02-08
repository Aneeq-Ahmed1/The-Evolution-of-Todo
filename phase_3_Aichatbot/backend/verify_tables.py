#!/usr/bin/env python
"""
Verification script to check if database tables exist in Neon PostgreSQL
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import inspect
from phase_2_web.backend.db import engine
from phase_2_web.backend import models  # Import models to register them
from sqlmodel import SQLModel

def verify_tables():
    """
    Verify that database tables exist and are accessible
    """
    print("Verifying database tables...")

    # Check what tables are registered in metadata
    registered_tables = list(SQLModel.metadata.tables.keys())
    print(f"Registered tables in metadata: {registered_tables}")

    # Connect to database and inspect existing tables
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"Tables found in database: {existing_tables}")

        # Check for expected tables (both singular and plural forms)
        expected_user_tables = ['user', 'users']
        expected_task_tables = ['task', 'tasks']

        user_table_found = any(table in existing_tables for table in expected_user_tables)
        task_table_found = any(table in existing_tables for table in expected_task_tables)

        print(f"\nUser table found: {user_table_found}")
        print(f"Task table found: {task_table_found}")

        if user_table_found and task_table_found:
            print("\n[SUCCESS]: Both user and task tables exist in the database!")

            # Show table details
            for table_name in existing_tables:
                if table_name in expected_user_tables + expected_task_tables:
                    columns = inspector.get_columns(table_name)
                    print(f"\nTable '{table_name}' columns:")
                    for col in columns:
                        print(f"  - {col['name']} ({col['type']})")
        else:
            print("\n[WARNING]: Expected tables not found in the database!")
            print("This could mean:")
            print("  1. Tables haven't been created yet")
            print("  2. Different table names are being used")
            print("  3. Database connection is to a different database than expected")

        return user_table_found and task_table_found

    except Exception as e:
        print(f"[ERROR]: Could not connect to database or inspect tables: {str(e)}")
        return False

def create_tables_if_missing():
    """
    Create tables if they don't exist
    """
    print("\nCreating tables if they don't exist...")
    try:
        SQLModel.metadata.create_all(engine)
        print("[SUCCESS]: Tables creation process completed!")
        return True
    except Exception as e:
        print(f"[ERROR]: Could not create tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("Database Table Verification Script")
    print("=" * 40)

    # First, try to verify existing tables
    tables_exist = verify_tables()

    if not tables_exist:
        print("\nTrying to create tables...")
        create_tables_if_missing()
        print("\nRe-verifying tables after creation attempt...")
        verify_tables()

    print("\nVerification complete!")