import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.api.chat_api import ChatRequest, chat_endpoint
from backend.src.db.database import get_session
from backend.auth import get_current_user, TokenData
from sqlmodel import Session

async def test_chat_endpoint():
    print("Testing chat endpoint directly...")
    
    # Create mock request
    request = ChatRequest(message="Hello, are you working?", conversation_id=None)
    
    # Create mock background tasks
    background_tasks = AsyncMock()
    
    # Create a real session
    session_gen = get_session()
    session = next(session_gen)
    
    # Create mock current user
    current_user = TokenData(user_id="185ebad3-6b57-4b29-a8f8-2ae2db9dda86", email="testuser@example.com")
    
    try:
        # Call the endpoint
        print("Calling chat endpoint...")
        response = await chat_endpoint(
            request=request,
            background_tasks=background_tasks,
            session=session,
            current_user=current_user
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    asyncio.run(test_chat_endpoint())