import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from backend.db import engine
from sqlalchemy import text

print("Connecting to database...")
print(f"Engine URL: {engine.url}")

try:
    with engine.connect() as conn:
        print("Connected successfully!")
        
        # Check if message table exists
        result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'message');"))
        message_table_exists = result.scalar()
        print(f"Message table exists: {message_table_exists}")
        
        if message_table_exists:
            print("\nColumns in message table:")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'message' 
                ORDER BY ordinal_position
            """))
            for row in result:
                print(f'  {row[0]}: {row[1]}, nullable={row[2]}')
        else:
            print("\nMessage table does not exist!")
            
        # Also check conversation table
        result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'conversation');"))
        conv_table_exists = result.scalar()
        print(f"\nConversation table exists: {conv_table_exists}")
        
        if conv_table_exists:
            print("\nColumns in conversation table:")
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'conversation' 
                ORDER BY ordinal_position
            """))
            for row in result:
                print(f'  {row[0]}: {row[1]}, nullable={row[2]}')
                
except Exception as e:
    print(f"Error connecting to database: {e}")
    import traceback
    traceback.print_exc()