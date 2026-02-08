#!/usr/bin/env python3
"""
Script to start the backend server with proper error handling
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

print("Starting AI Agent Platform backend server...")
print("Visit http://localhost:8000 after startup completes")
print("Press Ctrl+C to stop the server\n")

try:
    from main import app
    import uvicorn

    print("App imported successfully, starting server...")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["."],
        log_level="info"
    )

except KeyboardInterrupt:
    print("\nServer stopped by user")
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()