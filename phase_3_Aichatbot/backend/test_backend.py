#!/usr/bin/env python3
"""
Simple test script to check if the backend can be imported and run
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

print("Testing backend import...")

try:
    # Import the main app
    import main
    print("SUCCESS: Successfully imported main module")

    # Check if app exists
    if hasattr(main, 'app'):
        print("SUCCESS: FastAPI app found")

        # Check if routes can be imported
        try:
            from routes import tasks, auth
            print("SUCCESS: Routes imported successfully")
        except ImportError as e:
            print(f"ERROR: Failed to import routes: {e}")

    else:
        print("ERROR: No app attribute found in main module")

except Exception as e:
    print(f"ERROR: Error importing main module: {e}")
    import traceback
    traceback.print_exc()

print("\nBackend test completed.")