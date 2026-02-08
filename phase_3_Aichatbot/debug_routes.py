"""
Debug script to print all registered routes in the FastAPI application
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.main import app

def print_routes():
    print("Registered routes:")
    for route in app.routes:
        # Check if it's an APIRoute (has path attribute)
        if hasattr(route, 'path'):
            print(f"PATH: {route.path}, METHODS: {getattr(route, 'methods', 'N/A')}")
        else:
            print(f"ROUTE: {route}")

if __name__ == "__main__":
    print_routes()