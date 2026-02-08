import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

print("Testing individual components...")

try:
    print("Testing import of chat API...")
    from src.api.chat_api import ChatRequest, ChatResponse
    print("+ Chat API models imported successfully")
    
    print("Testing import of conversation service...")
    from src.services.conversation_service import ConversationService
    print("+ Conversation service imported successfully")
    
    print("Testing import of async database...")
    from src.db.async_database import async_engine
    from sqlmodel.ext.asyncio.session import AsyncSession
    print("+ Async database components imported successfully")
    
    print("All components imported successfully!")
    
    # Test creating an async session
    import asyncio
    
    async def test_async_session():
        print("Testing async session creation...")
        async with AsyncSession(async_engine) as session:
            print("+ Async session created successfully")
            return True
    
    # Run the async test
    success = asyncio.run(test_async_session())
    if success:
        print("+ All tests passed!")
    else:
        print("- Async session test failed")
        
except Exception as e:
    print(f"- Error during component testing: {e}")
    import traceback
    traceback.print_exc()