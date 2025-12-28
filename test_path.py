import os
from datetime import datetime

# Test the path that the manager is using
home_dir = os.path.expanduser("~")
data_file = os.path.join(home_dir, ".todo_app_data.json")

print(f"Home directory: {home_dir}")
print(f"Data file path: {data_file}")
print(f"Does file exist: {os.path.exists(data_file)}")

# Let's also try to create and write to the file to test permissions
try:
    with open(data_file, 'w') as f:
        f.write('{"test": "data"}')
    print("Successfully wrote test data")

    # Read it back
    with open(data_file, 'r') as f:
        content = f.read()
    print(f"Read back: {content}")

    # Clean up
    os.remove(data_file)
    print("Cleaned up test file")

except Exception as e:
    print(f"Error with file operations: {e}")