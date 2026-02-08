#!/usr/bin/env python3
"""
Migration script to update the conversation table schema
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from db import engine

def add_metadata_json_column():
    """
    Add the metadata_json column to the conversation table if it doesn't exist
    """
    print("Checking if metadata_json column exists in conversation table...")
    
    # Check if the column exists
    with engine.connect() as conn:
        # Query to check if the column exists in PostgreSQL
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'conversation' AND column_name = 'metadata_json'
        """))
        
        column_exists = result.fetchone() is not None
        
        if column_exists:
            print("+ metadata_json column already exists in conversation table")
            return
        
        print("- metadata_json column does not exist, adding it now...")
        
        # Add the metadata_json column as JSON type
        alter_query = text("ALTER TABLE conversation ADD COLUMN metadata_json JSON")
        conn.execute(alter_query)
        conn.commit()
        
        print("+ metadata_json column added successfully")
        

if __name__ == "__main__":
    add_metadata_json_column()