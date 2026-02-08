#!/usr/bin/env python3
"""
Comprehensive debug script to check settings loading and database configuration
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("=== COMPREHENSIVE SETTINGS DEBUG ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Backend directory: {backend_dir}")

# Check if .env file exists
env_file = backend_dir / ".env"
print(f".env file exists: {env_file.exists()}")

# Check if environment variable is set
print(f"DATABASE_URL from os.environ: {os.environ.get('DATABASE_URL', 'NOT SET IN ENV')}")
print(f"BETTER_AUTH_SECRET from os.environ: {'SET' if os.environ.get('BETTER_AUTH_SECRET') else 'NOT SET IN ENV'}")

# Try to import and check the settings
try:
    print("\n--- Attempting to import settings from backend.settings ---")
    from settings import settings as main_settings
    print(f"Imported settings object: {type(main_settings)}")
    print(f"DATABASE_URL from main settings: {main_settings.DATABASE_URL}")
    print(f"Settings file location: {main_settings.__class__.__module__}")
    
    # Check if it's PostgreSQL
    if main_settings.DATABASE_URL.startswith("postgresql"):
        print("+ Main settings: Using PostgreSQL database")
    elif main_settings.DATABASE_URL.startswith("sqlite"):
        print("- Main settings: Using SQLite database - THIS IS THE PROBLEM!")
    else:
        print(f"? Main settings: Unknown database type: {main_settings.DATABASE_URL}")
        
except Exception as e:
    print(f"- Error loading main settings: {e}")
    import traceback
    traceback.print_exc()

# Also check the src.db settings
try:
    print("\n--- Attempting to import settings from src.db.settings ---")
    from src.db.settings import settings as db_settings
    print(f"Imported db settings object: {type(db_settings)}")
    print(f"DATABASE_URL from db settings: {db_settings.database_url}")
    print(f"DB Settings file location: {db_settings.__class__.__module__}")
    
    # Check if it's PostgreSQL
    if db_settings.database_url.startswith("postgresql"):
        print("+ DB settings: Using PostgreSQL database")
    elif db_settings.database_url.startswith("sqlite"):
        print("- DB settings: Using SQLite database - THIS IS THE PROBLEM!")
    else:
        print(f"? DB settings: Unknown database type: {db_settings.database_url}")
        
except Exception as e:
    print(f"- Error loading db settings: {e}")
    import traceback
    traceback.print_exc()

# Check the db.py engine configuration
try:
    print("\n--- Checking db.py engine configuration ---")
    from db import engine
    print(f"Engine URL: {engine.url}")
    print(f"Engine dialect: {engine.dialect.name}")
    
    if 'postgresql' in str(engine.url):
        print("+ Engine: Connected to PostgreSQL")
    elif 'sqlite' in str(engine.url):
        print("- Engine: Connected to SQLite - THIS IS THE PROBLEM!")
    else:
        print(f"? Engine: Unknown dialect: {engine.dialect.name}")
        
except Exception as e:
    print(f"- Error checking db engine: {e}")
    import traceback
    traceback.print_exc()