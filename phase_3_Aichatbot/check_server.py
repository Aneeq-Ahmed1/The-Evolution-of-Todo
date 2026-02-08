import time
import urllib.request
import urllib.error

# Wait a bit for the server to start
time.sleep(5)

print("Checking if server is running...")

try:
    response = urllib.request.urlopen('http://localhost:8000/')
    print(f"Server is running! Status code: {response.getcode()}")
    print(f"Response: {response.read().decode('utf-8')[:100]}...")
except urllib.error.URLError as e:
    print(f"Server is not accessible: {e}")
except Exception as e:
    print(f"Error checking server: {e}")