#!/usr/bin/env python3
"""
Check the actual database schema for the conversation table
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from db import engine

def check_conversation_table_schema():
    """
    Check the actual schema of the conversation table
    """
    print("Checking conversation table schema...")
    
    with engine.connect() as conn:
        # Get all columns in the conversation table
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'conversation'
            ORDER BY ordinal_position
        """))
        
        columns = result.fetchall()
        
        print(f"Columns in conversation table ({len(columns)} total):")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
        
        print("\nChecking if there are multiple conversation-related tables...")
        # Check for any tables that might contain 'conversation'
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name LIKE '%conversation%'
        """))
        
        tables = result.fetchall()
        print(f"Conversation-related tables: {[t[0] for t in tables]}")
        
        # Also check for any tables that might have similar names
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name IN ('conversations', 'conversation')
        """))
        
        all_tables = result.fetchall()
        print(f"All conversation tables: {[t[0] for t in all_tables]}")


if __name__ == "__main__":
    check_conversation_table_schema()