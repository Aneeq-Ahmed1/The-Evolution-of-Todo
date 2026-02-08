import requests
import json

# Test the auth and chat endpoints
def test_auth_and_chat():
    base_url = "http://localhost:8000"
    
    # Try to register a test user (form data as per schema)
    register_payload = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Attempt registration
        register_response = requests.post(f"{base_url}/api/register", data=register_payload)
        print(f"Registration Status: {register_response.status_code}")
        print(f"Registration Response: {register_response.text}")
        
        # If registration fails due to user already existing, try login
        if register_response.status_code != 200:
            login_payload = {
                "email": "testuser@example.com",
                "password": "testpassword123"
            }
            login_response = requests.post(f"{base_url}/api/login", data=login_payload)
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response: {login_response.text}")
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                access_token = token_data.get("access_token")
                print("Login successful, got token")
            else:
                print(f"Login failed: {login_response.text}")
                return
        else:
            # Registration successful
            token_data = register_response.json()
            access_token = token_data.get("access_token")
            print("Registration successful, got token")
        
        # Now test the chat endpoint with the token
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        chat_payload = {
            "message": "Hello, are you working now?",
            "conversation_id": None
        }
        
        chat_response = requests.post(f"{base_url}/api/chat", json=chat_payload, headers=headers)
        print(f"Chat Endpoint Status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            print(f"SUCCESS! Chat response: {chat_data['response']}")
        else:
            print(f"Chat failed: {chat_response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    print("Testing auth and chat endpoints...")
    test_auth_and_chat()