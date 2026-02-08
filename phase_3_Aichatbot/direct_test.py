#!/usr/bin/env python3
"""
Direct test of the chat functionality to isolate the issue
"""
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.api.chat_api import chat_endpoint
from backend.src.models.message import MessageCreate
from backend.src.services.conversation_service import ConversationService
from backend.src.agents.orchestrator_agent import OrchestratorAgent
from backend.src.agents.chat_agent import ChatAgent
from backend.src.providers.gemini_adapter import GeminiProvider
from backend.src.db.database import get_session
from backend.settings import settings
from backend.auth import get_current_user
from sqlmodel import Session
from uuid import UUID

async def test_direct():
    print("Testing direct import and initialization...")
    
    try:
        # Check if settings are loaded correctly
        print(f"GEMINI_API_KEY loaded: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
        print(f"OPENAI_API_KEY loaded: {'Yes' if settings.OPENAI_API_KEY else 'No'}")
        print(f"LLM_PROVIDER selected: {settings.LLM_PROVIDER}")
        
        # Check if we can create a provider
        if settings.LLM_PROVIDER == "gemini":
            if settings.GEMINI_API_KEY:
                print("Creating Gemini provider...")
                provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
                print(f"Provider created: {provider}")
            else:
                print("No Gemini API key found")
                
        # Test basic functionality
        print("All imports successful!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct())