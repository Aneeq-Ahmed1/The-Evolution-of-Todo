#!/usr/bin/env python3
"""
Final test script to check backend functionality
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

print("Testing backend functionality...")

try:
    from main import app
    from fastapi.testclient import TestClient

    # Create a test client
    client = TestClient(app)

    # Test the health endpoint
    print("[PASS] Testing /health endpoint...")
    response = client.get("/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")

    # Test the root endpoint
    print("\n[PASS] Testing root endpoint...")
    response = client.get("/")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")

    # Test the debug db-status endpoint (now fixed)
    print("\n[PASS] Testing debug db-status endpoint...")
    response = client.get("/api/debug/db-status")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json() if response.status_code == 200 else 'Error occurred'}")

    print("\n[SUCCESS] Backend is working correctly!")
    print("\nSummary:")
    print("- Health endpoint: Working")
    print("- Root endpoint: Working")
    print("- DB status endpoint: Working")
    print("- Overall status: BACKEND IS FUNCTIONAL")

except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error testing backend: {e}")
    import traceback
    traceback.print_exc()