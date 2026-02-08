import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

print("Testing imports...")

try:
    # Test importing the modules that might have issues
    print("Importing settings...")
    from settings import settings
    print("Settings imported successfully")
    
    print("Importing db...")
    from db import engine
    print("DB imported successfully")
    
    print("Importing main...")
    from main import app
    print("Main app imported successfully")
    
    print("Importing chat API...")
    from src.api.chat_api import router as chat_router
    print("Chat API imported successfully")
    
    print("All imports successful!")
    
    # Test the database connection
    print("Testing database connection...")
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test;"))
        test_value = result.scalar()
        print(f"Database connection test result: {test_value}")
        
    print("Database connection successful!")
    
except Exception as e:
    print(f"Error during import/connection test: {e}")
    import traceback
    traceback.print_exc()