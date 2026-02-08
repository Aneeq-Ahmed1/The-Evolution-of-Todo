import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

print("Testing chat functionality directly...")

try:
    # Import the necessary modules
    from src.api.chat_api import ChatRequest
    from src.db.async_database import get_async_session
    from auth import get_current_user
    from src.services.conversation_service import ConversationService
    
    # Create a mock token data
    class MockTokenData:
        user_id = "8aceb0f5-6072-4d9f-a032-b3b515b856ef"
    
    # Create a mock request
    chat_request = ChatRequest(message="hi")
    
    print("All imports successful, testing conversation creation...")
    
    # Test creating a conversation service
    import asyncio
    from sqlmodel.ext.asyncio.session import AsyncSession
    
    async def test_conversation_creation():
        async with get_async_session() as session:
            conversation_service = ConversationService(session)
            
            # Try to create a conversation
            conversation = await conversation_service.create_conversation(
                user_id=MockTokenData.user_id,
                title="Test conversation"
            )
            
            print(f"Conversation created successfully: {conversation.id}")
            return conversation
            
    # Run the async test
    conversation = asyncio.run(test_conversation_creation())
    print("Direct test successful!")
    
except Exception as e:
    print(f"Error in direct test: {e}")
    import traceback
    traceback.print_exc()