#!/usr/bin/env python3
"""
Migration script to update the message table schema with missing columns
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from db import engine

def add_missing_columns():
    """
    Add all missing columns to the message table if they don't exist
    """
    print("Checking for missing columns in message table...")

    with engine.connect() as conn:
        # Check if tool_calls column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'message' AND column_name = 'tool_calls'
        """))

        tool_calls_exists = result.fetchone() is not None

        if tool_calls_exists:
            print("+ tool_calls column already exists in message table")
        else:
            print("- tool_calls column does not exist, adding it now...")
            # Add the tool_calls column as JSON type
            alter_query = text("ALTER TABLE message ADD COLUMN tool_calls JSON")
            conn.execute(alter_query)
            print("+ tool_calls column added successfully")

        # Check if tool_response column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'message' AND column_name = 'tool_response'
        """))

        tool_response_exists = result.fetchone() is not None

        if tool_response_exists:
            print("+ tool_response column already exists in message table")
        else:
            print("- tool_response column does not exist, adding it now...")
            # Add the tool_response column as JSON type
            alter_query = text("ALTER TABLE message ADD COLUMN tool_response JSON")
            conn.execute(alter_query)
            print("+ tool_response column added successfully")

        # Check if timestamp column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'message' AND column_name = 'timestamp'
        """))

        timestamp_exists = result.fetchone() is not None

        if timestamp_exists:
            print("+ timestamp column already exists in message table")
        else:
            print("- timestamp column does not exist, adding it now...")
            # Add the timestamp column with default value
            alter_query = text("ALTER TABLE message ADD COLUMN timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()")
            conn.execute(alter_query)
            print("+ timestamp column added successfully")

        conn.commit()
        print("All missing columns have been added successfully!")


if __name__ == "__main__":
    add_missing_columns()