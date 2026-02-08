#!/usr/bin/env python3
"""
Debug script to check environment variables and database configuration
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("Checking environment variables...")
print(f"Current working directory: {os.getcwd()}")
print(f"Backend directory: {backend_dir}")

# Check if .env file exists
env_file = backend_dir / ".env"
print(f".env file exists: {env_file.exists()}")

if env_file.exists():
    print("\nContents of .env file:")
    with open(env_file, 'r') as f:
        print(f.read())

print(f"\nDATABASE_URL from environment: {os.environ.get('DATABASE_URL', 'NOT SET')}")

try:
    from settings import settings
    print(f"\nDATABASE_URL from settings: {settings.DATABASE_URL}")
    
    # Check if it's PostgreSQL
    if settings.DATABASE_URL.startswith("postgresql"):
        print("Using PostgreSQL database")
    elif settings.DATABASE_URL.startswith("sqlite"):
        print("Using SQLite database - THIS IS THE PROBLEM!")
    else:
        print(f"Unknown database type: {settings.DATABASE_URL}")
        
except Exception as e:
    print(f"Error loading settings: {e}")
    import traceback
    traceback.print_exc()