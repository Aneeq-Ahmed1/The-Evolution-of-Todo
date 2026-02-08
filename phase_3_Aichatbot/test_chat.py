import requests
import time
import json

# Wait a bit for the server to start
time.sleep(3)

print("Testing chat functionality...")

# First, let's try to login to get a valid token (assuming there's a test user)
try:
    # Try to make a simple request to the chat endpoint with a valid token
    # We'll use the token from the error log you showed earlier
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjhhY2ViMGY1LTYwNzItNGQ5Zi1hMDMyLWIzYjUxNWI4NTZlZiIsImVtYWlsIjoiYW5lZXExMjM0NTZAZ21haWwuY29tIiwiZXhwIjoxNzcwNTU2MjE2fQ.dC0iOSyr-EOnLWtpKoshcewKgxd5hENVKgWjpeSX01U',
        'Content-Type': 'application/json'
    }
    
    chat_payload = {
        "message": "hi"
    }
    
    print("Sending chat message: 'hi'")
    response = requests.post("http://localhost:8000/api/chat", 
                             headers=headers, 
                             json=chat_payload,
                             timeout=30)
    
    print(f"Chat endpoint status: {response.status_code}")
    if response.status_code == 200:
        print(f"Chat response: {response.json()}")
    else:
        print(f"Chat error response: {response.text}")
        
except Exception as e:
    print(f"Error testing chat: {e}")
    import traceback
    traceback.print_exc()