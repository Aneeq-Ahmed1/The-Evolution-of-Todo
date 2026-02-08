"""
Chat API endpoint for the AI Agent Platform
Implements the user-specific chat endpoint at /api/{user_id}/chat
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import Dict, Any, Optional
from uuid import UUID
import uuid
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from datetime import datetime
import logging

from src.models.conversation import ConversationCreate, ConversationRead
from src.models.message import MessageCreate, MessageRead
from src.services.conversation_service import ConversationService
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.chat_agent import ChatAgent
from src.providers.gemini_adapter import GeminiProvider
from db import get_session
from src.db.async_database import get_async_session
from auth import get_current_user, verify_user_id_match, TokenData
from settings import settings
from src.utils.logging import log_request, Logger
from src.middleware.rate_limiter import check_rate_limit


router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    conversation_id: Optional[str] = None  # Will be converted to UUID if provided
    model: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    tool_calls: list[Dict[str, Any]] = []
    message_id: int
    timestamp: datetime
    conversation_id: str


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def user_specific_chat_endpoint(
    user_id: str,
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)  # Using sync session for basic validation
):
    """
    User-specific chat endpoint for interacting with the AI agent
    Ensures user isolation: only the authenticated user can access their own conversations
    Loads complete conversation history to maintain context
    """
    try:
        # Verify that the user_id in the JWT matches the user_id in the URL
        verify_user_id_match(current_user.user_id, user_id)
        
        # Log the request with authenticated user ID
        Logger.info(f"User-specific chat endpoint received message from user: {user_id[:8]}..., message: {request.message[:50]}...")
        log_request(user_id, f"/api/{user_id}/chat", "POST")

        # Check rate limits
        await check_rate_limit(user_id)

        # Initialize services with async session
        from src.db.async_database import async_engine
        from sqlmodel.ext.asyncio.session import AsyncSession

        async with AsyncSession(async_engine) as async_session:
            conversation_service = ConversationService(async_session)

            # Initialize provider based on configuration
            if settings.LLM_PROVIDER == "gemini":
                if not settings.GEMINI_API_KEY:
                    Logger.warning("Gemini API key not configured, using mock provider for testing")
                    from ..src.providers.mock_provider import MockProvider
                    provider = MockProvider()
                else:
                    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
            elif settings.LLM_PROVIDER == "openai":
                if not settings.OPENAI_API_KEY:
                    Logger.warning("OpenAI API key not configured, using mock provider for testing")
                    from ..src.providers.mock_provider import MockProvider
                    provider = MockProvider()
                else:
                    from ..src.providers.openai_adapter import OpenAIProvider
                    provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
            else:
                # Default to Gemini if provider not recognized, but use mock if no key
                if settings.GEMINI_API_KEY:
                    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
                elif settings.OPENAI_API_KEY:
                    from ..src.providers.openai_adapter import OpenAIProvider
                    provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
                else:
                    Logger.warning("No LLM provider API key configured, using mock provider for testing")
                    from ..src.providers.mock_provider import MockProvider
                    provider = MockProvider()

            # Validate provider configuration
            if not provider.validate_config():
                Logger.error("Provider configuration validation failed")
                raise HTTPException(status_code=500, detail="Provider configuration validation failed - check API key and model access")

            # Initialize agents
            chat_agent = ChatAgent(conversation_service, provider)
            orchestrator_agent = OrchestratorAgent(conversation_service)

            # Register the chat agent with the orchestrator for general conversation
            orchestrator_agent.register_agent("general", chat_agent)
            orchestrator_agent.register_agent("chat", chat_agent)
            orchestrator_agent.register_agent("converse", chat_agent)

            # Get or create conversation
            conversation_id = request.conversation_id
            if not conversation_id:
                # Create a new conversation
                Logger.info(f"Creating new conversation for user: {user_id[:8]}...")
                try:
                    # Ensure user_id is properly handled as UUID
                    user_uuid = UUID(user_id) if is_valid_uuid(user_id) else uuid.uuid4()
                    conversation = await conversation_service.create_conversation(
                        user_id=user_uuid,
                        title=request.message[:50] + "..." if len(request.message) > 50 else request.message
                    )
                    conversation_id = str(conversation.id)
                    Logger.info(f"Created new conversation with ID: {conversation_id}")
                except Exception as db_error:
                    Logger.error(f"Database error creating conversation: {str(db_error)}", exc_info=True)
                    raise HTTPException(status_code=500, detail="Failed to create conversation in database")
            else:
                # Validate that the conversation exists
                Logger.info(f"Using existing conversation ID: {conversation_id}")
                try:
                    # The conversation service now handles both string and UUID types
                    existing_conversation = await conversation_service.get_conversation(conversation_id)
                    if not existing_conversation:
                        Logger.error(f"Conversation not found: {conversation_id}")
                        raise HTTPException(status_code=404, detail="Conversation not found")

                    # Verify that the conversation belongs to the current user
                    if str(existing_conversation.user_id) != user_id:
                        raise HTTPException(
                            status_code=403,
                            detail="Access forbidden: You don't have permission to access this conversation"
                        )
                except Exception as db_error:
                    Logger.error(f"Database error retrieving conversation: {str(db_error)}", exc_info=True)
                    raise HTTPException(status_code=500, detail="Failed to retrieve conversation from database")

            # Load complete conversation history to maintain context
            Logger.info(f"Loading conversation history for conversation: {conversation_id}")
            # Pass the conversation_id directly (the service now handles both string and UUID)
            conversation_history = await conversation_service.get_messages_for_conversation(conversation_id)
            
            # Add the user's message to the conversation before processing
            user_message = MessageCreate(
                role="user", 
                content=request.message, 
                user_id=user_id
            )
            user_message_record = await conversation_service.add_message_to_conversation(
                conversation_id, 
                user_message
            )

            # Process the message through the orchestrator
            Logger.info(f"Processing message through orchestrator agent for conversation: {conversation_id[:8]}...")
            try:
                # The chat agent should internally load and use the conversation history
                # when processing the message, which it already does in the current implementation
                agent_response = await orchestrator_agent.process(
                    message=request.message,
                    conversation_id=conversation_id,  # Pass original string ID to orchestrator
                    user_id=user_id
                )

                if agent_response.error:
                    Logger.error(f"Agent processing error: {agent_response.error}")
                    raise HTTPException(status_code=500, detail=agent_response.error)

                Logger.info(f"Agent response generated successfully for conversation: {conversation_id[:8]}...")
                
                # Add the assistant's response to the conversation
                assistant_message = MessageCreate(
                    role="assistant",
                    content=agent_response.content,
                    user_id=user_id,  # Include user_id for assistant messages too
                    tool_calls=agent_response.tool_calls
                )
                assistant_message_record = await conversation_service.add_message_to_conversation(
                    conversation_id, 
                    assistant_message
                )

            except Exception as ai_error:
                Logger.error(f"AI processing error: {str(ai_error)}", exc_info=True)
                raise HTTPException(status_code=500, detail="Failed to generate AI response")

            # Prepare the response
            response = ChatResponse(
                response=agent_response.content,
                tool_calls=agent_response.tool_calls or [],
                message_id=int(datetime.utcnow().timestamp()),  # Simple message ID based on timestamp
                timestamp=datetime.utcnow(),
                conversation_id=conversation_id
            )

            return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        import sys
        Logger.error(f"HTTPException in user-specific chat endpoint: {str(sys.exc_info()[1])}", exc_info=True)
        raise
    except Exception as e:
        Logger.error(f"Unexpected error in user-specific chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


def is_valid_uuid(uuid_str: str) -> bool:
    """
    Check if a string is a valid UUID

    Args:
        uuid_str: String to check

    Returns:
        bool: True if valid UUID, False otherwise
    """
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False


# Health check endpoint
@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "user-specific-chat-api"}