import requests
import json

# Test the chat endpoint
def test_chat_endpoint():
    url = "http://localhost:8000/api/chat"
    
    # Sample payload (without authentication for now)
    payload = {
        "message": "Hello, are you working now?",
        "conversation_id": None
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response: {data['response']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    print("Testing chat endpoint...")
    test_chat_endpoint()