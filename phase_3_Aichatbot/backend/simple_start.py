#!/usr/bin/env python3
"""
Simple script to start the backend server with error handling
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

print("Attempting to start backend server...")

try:
    # Import and run the main app
    from main import app
    import uvicorn

    print("App imported successfully, starting server...")

    # Run the server with minimal configuration
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error running server: {e}")
    import traceback
    traceback.print_exc()