import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

print("Testing main app import...")

try:
    print("Importing main app...")
    from main import app
    print("Main app imported successfully")
    
    print("Testing if the app has the chat route...")
    # Check if the app has the chat routes
    for route in app.routes:
        if hasattr(route, 'path') and 'chat' in route.path:
            print(f"Found chat route: {route.path}")
    
    print("Main app test completed successfully!")
    
except Exception as e:
    print(f"Error importing main app: {e}")
    import traceback
    traceback.print_exc()