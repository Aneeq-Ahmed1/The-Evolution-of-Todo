#!/usr/bin/env python3
"""
Simple script to run the backend server
"""

import os
import sys
from contextlib import suppress

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Suppress the warnings about database info not being available
import warnings
import re
warnings.filterwarnings("ignore", message=".*current_database.*")
warnings.filterwarnings("ignore", message=".*current_schema.*")
warnings.filterwarnings("ignore", message=".*neon.branch_name.*")

def run_server():
    try:
        from main import app
        import uvicorn

        print("Starting AI Agent Platform backend server...")
        print("Visit http://localhost:8000 after startup completes")
        print("Press Ctrl+C to stop the server\n")

        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,
            reload_dirs=["."]
        )

    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_server()