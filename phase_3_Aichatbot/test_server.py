import requests
import time

# Wait a bit for the server to start
time.sleep(3)

print("Testing server connection...")

try:
    # Test basic connectivity
    response = requests.get("http://localhost:8000/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint response: {response.json()}")
    
    # Test health endpoint
    health_response = requests.get("http://localhost:8000/health")
    print(f"Health endpoint status: {health_response.status_code}")
    print(f"Health endpoint response: {health_response.json()}")
    
    # Test database status endpoint
    db_response = requests.get("http://localhost:8000/api/debug/db-status")
    print(f"DB Status endpoint status: {db_response.status_code}")
    if db_response.status_code == 200:
        print(f"DB Status response: {db_response.json()}")
    else:
        print(f"DB Status error: {db_response.text}")
        
except Exception as e:
    print(f"Error testing server: {e}")