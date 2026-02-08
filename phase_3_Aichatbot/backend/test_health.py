#!/usr/bin/env python3
"""
Test script to check backend health without starting the full server
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

print("Testing backend health endpoint...")

try:
    from main import app
    from fastapi.testclient import TestClient

    # Create a test client
    client = TestClient(app)

    # Test the health endpoint
    print("Testing /health endpoint...")
    response = client.get("/health")
    print(f"Health endpoint status: {response.status_code}")
    print(f"Health endpoint response: {response.json()}")

    # Test the root endpoint
    print("\nTesting root endpoint...")
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint response: {response.json()}")

    # Test the debug db-status endpoint
    print("\nTesting debug db-status endpoint...")
    response = client.get("/api/debug/db-status")
    print(f"DB status endpoint status: {response.status_code}")
    print(f"DB status endpoint response: {response.json()}")

    print("\nBackend is working correctly!")

except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error testing backend: {e}")
    import traceback
    traceback.print_exc()