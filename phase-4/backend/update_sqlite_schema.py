#!/usr/bin/env python3
"""
Script to update the SQLite database schema to match the current model.
This addresses the schema mismatch issue where the database doesn't have
the advanced fields that were added to the Task model.
"""

import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or not DATABASE_URL.startswith("sqlite:///"):
    print("Error: DATABASE_URL not found or not SQLite format in environment variables")
    exit(1)

# Extract database file path from URL
db_path = DATABASE_URL.replace("sqlite:///", "")

print(f"Connecting to SQLite database: {db_path}")

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the columns exist and add them if they don't
    print("Checking and adding missing columns to the task table...")

    # Check if priority column exists, if not add it
    cursor.execute("PRAGMA table_info(task)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'priority' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'medium'")
        print("Added 'priority' column")
    else:
        print("'priority' column already exists")

    if 'tags' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN tags TEXT")
        print("Added 'tags' column")
    else:
        print("'tags' column already exists")

    if 'category' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN category TEXT")
        print("Added 'category' column")
    else:
        print("'category' column already exists")

    if 'due_date' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN due_date TIMESTAMP")
        print("Added 'due_date' column")
    else:
        print("'due_date' column already exists")

    if 'due_time' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN due_time TEXT")
        print("Added 'due_time' column")
    else:
        print("'due_time' column already exists")

    if 'is_recurring' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN is_recurring BOOLEAN DEFAULT 0")
        print("Added 'is_recurring' column")
    else:
        print("'is_recurring' column already exists")

    if 'recurrence_pattern' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN recurrence_pattern TEXT")
        print("Added 'recurrence_pattern' column")
    else:
        print("'recurrence_pattern' column already exists")

    if 'recurrence_interval' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN recurrence_interval INTEGER DEFAULT 1")
        print("Added 'recurrence_interval' column")
    else:
        print("'recurrence_interval' column already exists")

    if 'next_occurrence' not in columns:
        cursor.execute("ALTER TABLE task ADD COLUMN next_occurrence TIMESTAMP")
        print("Added 'next_occurrence' column")
    else:
        print("'next_occurrence' column already exists")

    # Commit the changes
    conn.commit()
    print("\nSchema update completed successfully!")

    # Verify the columns were added
    print("\nVerifying columns in task table:")
    cursor.execute("PRAGMA table_info(task)")
    columns_info = cursor.fetchall()
    for col in columns_info:
        cid, name, col_type, notnull, default_value, pk = col
        print(f"  {name}: {col_type}, not_null: {bool(notnull)}, default: {default_value}")

except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

print("SQLite schema update script completed.")