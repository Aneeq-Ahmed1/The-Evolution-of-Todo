import requests
import time

# Wait a bit for the server to start
time.sleep(3)

print("Testing chat functionality...")

# Use a simple test without authorization to see if we get a different error
try:
    print("Sending unauthorized request to trigger error log...")
    headers = {
        'Content-Type': 'application/json'
    }
    
    chat_payload = {
        "message": "hi"
    }
    
    response = requests.post("http://localhost:8000/api/chat", 
                             headers=headers, 
                             json=chat_payload,
                             timeout=10)
    
    print(f"Chat endpoint status: {response.status_code}")
    print(f"Chat response: {response.text}")
        
except Exception as e:
    print(f"Error testing chat: {e}")