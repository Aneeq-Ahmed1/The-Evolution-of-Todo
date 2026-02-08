#!/usr/bin/env python3
"""
Script to update the database schema to match the current model.
This addresses the schema mismatch issue where the database doesn't have
the advanced fields that were added to the Task model.
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables")
    exit(1)

print(f"Connecting to database: {DATABASE_URL}")

try:
    # Parse the database URL
    import urllib.parse
    parsed_url = urllib.parse.urlparse(DATABASE_URL)

    # Connect to the database
    conn = psycopg2.connect(
        host=parsed_url.hostname,
        port=parsed_url.port,
        database=parsed_url.path[1:],  # Remove the leading '/'
        user=parsed_url.username,
        password=parsed_url.password,
        sslmode='require'
    )

    cursor = conn.cursor()

    # Check if the columns exist and add them if they don't
    print("Checking and adding missing columns to the task table...")

    # Check if priority column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='priority'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';
        """)
        print("Added 'priority' column")
    else:
        print("'priority' column already exists")

    # Check if tags column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='tags'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN tags VARCHAR(500);
        """)
        print("Added 'tags' column")
    else:
        print("'tags' column already exists")

    # Check if category column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='category'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN category VARCHAR(100);
        """)
        print("Added 'category' column")
    else:
        print("'category' column already exists")

    # Check if due_date column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='due_date'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN due_date TIMESTAMP;
        """)
        print("Added 'due_date' column")
    else:
        print("'due_date' column already exists")

    # Check if due_time column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='due_time'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN due_time VARCHAR(10);
        """)
        print("Added 'due_time' column")
    else:
        print("'due_time' column already exists")

    # Check if is_recurring column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='is_recurring'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE;
        """)
        print("Added 'is_recurring' column")
    else:
        print("'is_recurring' column already exists")

    # Check if recurrence_pattern column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='recurrence_pattern'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN recurrence_pattern VARCHAR(50);
        """)
        print("Added 'recurrence_pattern' column")
    else:
        print("'recurrence_pattern' column already exists")

    # Check if recurrence_interval column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='recurrence_interval'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN recurrence_interval INTEGER DEFAULT 1;
        """)
        print("Added 'recurrence_interval' column")
    else:
        print("'recurrence_interval' column already exists")

    # Check if next_occurrence column exists, if not add it
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='task' AND column_name='next_occurrence'
    """)
    if not cursor.fetchone():
        cursor.execute("""
            ALTER TABLE task ADD COLUMN next_occurrence TIMESTAMP;
        """)
        print("Added 'next_occurrence' column")
    else:
        print("'next_occurrence' column already exists")

    # Commit the changes
    conn.commit()
    print("\nSchema update completed successfully!")

    # Verify the columns were added
    print("\nVerifying columns in task table:")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'task'
        ORDER BY ordinal_position;
    """)

    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[0]}: {col[1]}, nullable: {col[2]}, default: {col[3]}")

except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

print("Schema update script completed.")