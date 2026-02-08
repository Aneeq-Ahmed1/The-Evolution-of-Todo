import os
import jwt
from datetime import datetime, timedelta
from backend.settings import settings

# Test if the secret is properly loaded
print(f"BETTER_AUTH_SECRET loaded: {'Yes' if settings.BETTER_AUTH_SECRET else 'No'}")
print(f"Secret length: {len(settings.BETTER_AUTH_SECRET) if settings.BETTER_AUTH_SECRET else 0}")
print(f"Secret preview: {settings.BETTER_AUTH_SECRET[:10] if settings.BETTER_AUTH_SECRET else 'None'}...")

# Create a test token
if settings.BETTER_AUTH_SECRET:
    test_payload = {
        "id": "test-user-id",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    test_token = jwt.encode(test_payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    print(f"Generated test token: {test_token[:30]}...")
    
    # Try to decode it
    try:
        decoded = jwt.decode(test_token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        print(f"Successfully decoded test token: {decoded}")
    except Exception as e:
        print(f"Failed to decode test token: {e}")
else:
    print("Cannot generate test token - no secret available")