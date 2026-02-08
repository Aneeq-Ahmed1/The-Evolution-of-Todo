"""
Test script to verify the conversation flow and ensure dynamic responses
"""
import asyncio
import os
from dotenv import load_dotenv
from unittest.mock import AsyncMock, MagicMock

# Load environment variables
load_dotenv()

from backend.src.agents.chat_agent import ChatAgent
from backend.src.services.conversation_service import ConversationService
from backend.src.providers.mock_provider import MockProvider
from backend.src.providers.gemini_adapter import GeminiProvider
from backend.src.providers.openai_adapter import OpenAIProvider
from backend.src.models.message import MessageCreate
from backend.src.db.async_database import async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid


async def test_conversation_flow():
    """
    Test the complete conversation flow to ensure dynamic responses
    """
    print("Testing conversation flow for dynamic responses...")
    
    # Create a mock conversation service
    async with AsyncSession(async_engine) as session:
        conversation_service = ConversationService(session)
        
        # Create a conversation
        user_id = str(uuid.uuid4())
        conversation = await conversation_service.create_conversation(
            user_id=user_id,
            title="Test Conversation"
        )
        conversation_id = str(conversation.id)
        print(f"Created conversation: {conversation_id}")
        
        # Determine which provider to use based on environment
        from backend.settings import settings
        
        if settings.LLM_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
            provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
        elif settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
        else:
            print("Using MockProvider since no API key is configured")
            provider = MockProvider()
        
        # Create the chat agent
        chat_agent = ChatAgent(conversation_service, provider)
        
        # Test multiple exchanges to verify conversation context is maintained
        test_messages = [
            "Hello, how are you?",
            "What did I just say?",
            "Can you remind me of my first message?",
            "Thanks for the help!"
        ]
        
        responses = []
        for i, msg in enumerate(test_messages):
            print(f"\n--- Exchange {i+1} ---")
            print(f"User: {msg}")
            
            # Process the message
            response = await chat_agent.process(
                message=msg,
                conversation_id=conversation_id,
                user_id=user_id
            )
            
            print(f"AI: {response.content}")
            responses.append(response.content)
            
            # Verify that the response is not static
            if i > 0 and response.content == responses[0]:
                print(f"WARNING: Response appears to be static! Got same response as first exchange.")
        
        print(f"\n--- Conversation Summary ---")
        print(f"Total exchanges: {len(test_messages)}")
        print(f"All responses unique: {len(set(responses)) == len(responses)}")
        
        # Get the conversation history to verify it was stored properly
        history = await conversation_service.get_conversation_history(conversation_id)
        print(f"Messages in conversation history: {len(history)}")
        
        for i, msg in enumerate(history):
            print(f"  {i+1}. [{msg.role}] {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")
        
        print("\nConversation flow test completed!")
        return True


if __name__ == "__main__":
    asyncio.run(test_conversation_flow())