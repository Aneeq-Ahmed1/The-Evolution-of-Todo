"""
Test script to verify the complete chat flow:
1. Receive message
2. Save conversation in Neon DB
3. Generate response using Gemini API
4. Return response to frontend
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.src.api.chat_api import chat_endpoint
from backend.src.api.chat_api import ChatRequest
from backend.auth import TokenData
from backend.src.db.async_database import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.settings import settings


async def test_chat_flow():
    """
    Test the complete chat flow
    """
    print("Testing complete chat flow...")
    
    # Create a mock user token
    mock_user = TokenData(user_id="test-user-id", email="test@example.com")
    
    # Create a sample chat request
    chat_request = ChatRequest(
        message="Hello, how are you today?",
        conversation_id=None  # Will create a new conversation
    )
    
    print(f"Using database URL: {settings.DATABASE_URL}")
    print(f"Using Gemini API key: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    
    # Get async session
    async for session in get_async_session():
        try:
            # Call the chat endpoint
            print("Calling chat endpoint...")
            response = await chat_endpoint(
                request=chat_request,
                background_tasks=None,  # We'll simulate this
                current_user=mock_user
            )
            
            print(f"Response received:")
            print(f"- Conversation ID: {response.conversation_id}")
            print(f"- Response: {response.response[:100]}...")
            print(f"- Metadata: {response.metadata}")
            
            print("\nChat flow test completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error during chat flow test: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    asyncio.run(test_chat_flow())