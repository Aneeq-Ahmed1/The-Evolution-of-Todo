"""
Chat API endpoint for the AI Agent Platform
Implements the main chat endpoint for interacting with the agent
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
from uuid import UUID
import uuid
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from ..models.conversation import ConversationCreate, ConversationRead
from ..models.message import MessageCreate, MessageRead
from ..services.conversation_service import ConversationService
from ..agents.orchestrator_agent import OrchestratorAgent
from ..agents.chat_agent import ChatAgent
from ..providers.gemini_adapter import GeminiProvider
from ..db.database import get_session
from ..db.async_database import get_async_session
# Handle the import differently to avoid relative import issues
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Now import using the absolute path
try:
    from auth import get_current_user, TokenData
    from settings import settings
except ImportError:
    # If direct import fails, try with backend prefix
    from backend.auth import get_current_user, TokenData
    from backend.settings import settings

from ..utils.logging import log_request, Logger
from ..middleware.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    conversation_id: Optional[str] = None  # Will be converted to UUID if provided


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    conversation_id: str
    metadata: Dict[str, Any]


class NewConversationRequest(BaseModel):
    """Request model for creating a new conversation"""
    initial_message: Optional[str] = None
    title: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: TokenData = Depends(get_current_user)
) -> ChatResponse:
    """
    Main chat endpoint for interacting with the AI agent
    Implements FR-001: System MUST provide a standardized interface that routes requests to configurable LLM providers
    Implements FR-005: System MUST provide a web-based chatbot UI for user interaction
    Implements FR-013: System MUST implement user authentication with session management for multi-user support and conversation privacy
    """
    print("CHAT ENDPOINT HIT")  # Emergency logging
    try:
        # Log the request with authenticated user ID
        user_id = current_user.user_id
        Logger.info(f"Chat endpoint received message from user: {user_id[:8]}..., message: {request.message[:50]}...")
        log_request(user_id, "/api/chat", "POST")

        # Check rate limits
        await check_rate_limit(user_id)

        # Initialize services with async session
        from ..db.async_database import async_engine
        from sqlmodel.ext.asyncio.session import AsyncSession

        async with AsyncSession(async_engine) as async_session:
            conversation_service = ConversationService(async_session)

            # Initialize provider based on configuration
            if settings.LLM_PROVIDER == "gemini":
                if not settings.GEMINI_API_KEY:
                    Logger.warning("Gemini API key not configured, using mock provider for testing")
                    from ..providers.mock_provider import MockProvider
                    provider = MockProvider()
                else:
                    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
            elif settings.LLM_PROVIDER == "openai":
                if not settings.OPENAI_API_KEY:
                    Logger.warning("OpenAI API key not configured, using mock provider for testing")
                    from ..providers.mock_provider import MockProvider
                    provider = MockProvider()
                else:
                    from ..providers.openai_adapter import OpenAIProvider
                    provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
            else:
                # Default to Gemini if provider not recognized, but use mock if no key
                if settings.GEMINI_API_KEY:
                    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
                elif settings.OPENAI_API_KEY:
                    from ..providers.openai_adapter import OpenAIProvider
                    provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
                else:
                    Logger.warning("No LLM provider API key configured, using mock provider for testing")
                    from ..providers.mock_provider import MockProvider
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
                    conversation_uuid = UUID(conversation_id)
                    existing_conversation = await conversation_service.get_conversation(conversation_uuid)
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

            # Process the message through the orchestrator
            Logger.info(f"Processing message through orchestrator agent for conversation: {conversation_id[:8]}...")
            try:
                agent_response = await orchestrator_agent.process(
                    message=request.message,
                    conversation_id=conversation_id,
                    user_id=user_id
                )

                if agent_response.error:
                    Logger.error(f"Agent processing error: {agent_response.error}")
                    raise HTTPException(status_code=500, detail=agent_response.error)

                Logger.info(f"Agent response generated successfully for conversation: {conversation_id[:8]}...")
            except Exception as ai_error:
                Logger.error(f"AI processing error: {str(ai_error)}", exc_info=True)
                raise HTTPException(status_code=500, detail="Failed to generate AI response")

            # Prepare the response
            response = ChatResponse(
                response=agent_response.content,
                conversation_id=conversation_id,
                metadata=agent_response.metadata
            )

            return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        import sys
        Logger.error(f"HTTPException in chat endpoint: {str(sys.exc_info()[1])}", exc_info=True)
        raise
    except Exception as e:
        Logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/conversations", response_model=list[ConversationRead])
async def get_conversations(
    current_user: TokenData = Depends(get_current_user),
    async_session: AsyncSession = Depends(get_async_session)
) -> list[ConversationRead]:
    """
    Get a list of conversations for the authenticated user
    Implements FR-013: System MUST implement user authentication with session management for multi-user support and conversation privacy
    """
    try:
        user_id = current_user.user_id
        log_request(user_id, "/api/conversations", "GET")

        conversation_service = ConversationService(async_session)
        conversations = await conversation_service.get_user_conversations(UUID(user_id))

        return conversations
    except Exception as e:
        Logger.error(f"Error getting conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve conversations")


@router.post("/conversations", response_model=ConversationRead)
async def create_conversation(
    request: NewConversationRequest,
    current_user: TokenData = Depends(get_current_user),
    async_session: AsyncSession = Depends(get_async_session)
) -> ConversationRead:
    """
    Create a new conversation
    Implements FR-005: System MUST provide a web-based chatbot UI for user interaction
    Implements FR-013: System MUST implement user authentication with session management for multi-user support and conversation privacy
    """
    try:
        user_id = current_user.user_id
        log_request(user_id, "/api/conversations", "POST")

        conversation_service = ConversationService(async_session)
        conversation = await conversation_service.create_conversation(
            user_id=UUID(user_id) if is_valid_uuid(user_id) else UUID(user_id),
            title=request.title
        )

        # If an initial message was provided, process it
        if request.initial_message:
            # Initialize provider and agents to process the initial message
            if settings.LLM_PROVIDER == "gemini":
                if not settings.GEMINI_API_KEY:
                    raise HTTPException(status_code=500, detail="Gemini API key not configured")
                provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
            else:
                if not settings.GEMINI_API_KEY:
                    raise HTTPException(status_code=500, detail="Default provider API key not configured")
                provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)

            # Create a new conversation service instance for the initial message processing
            temp_conversation_service = ConversationService(async_session)
            chat_agent = ChatAgent(temp_conversation_service, provider)
            orchestrator_agent = OrchestratorAgent(temp_conversation_service)
            orchestrator_agent.register_agent("general", chat_agent)

            # Process the initial message
            await orchestrator_agent.process(
                message=request.initial_message,
                conversation_id=str(conversation.id),
                user_id=user_id
            )

        return conversation
    except Exception as e:
        Logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create conversation")


@router.get("/conversations/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: str,
    current_user: TokenData = Depends(get_current_user),
    async_session: AsyncSession = Depends(get_async_session)
) -> ConversationRead:
    """
    Get a specific conversation by ID
    Implements FR-013: System MUST implement user authentication with session management for multi-user support and conversation privacy
    """
    try:
        user_id = current_user.user_id
        log_request(user_id, f"/api/conversations/{conversation_id}", "GET")

        conversation_service = ConversationService(async_session)
        conversation = await conversation_service.get_conversation(UUID(conversation_id))

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Verify that the conversation belongs to the current user
        if str(conversation.user_id) != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="Access forbidden: You don't have permission to access this conversation"
            )

        return conversation
    except HTTPException:
        raise
    except Exception as e:
        Logger.error(f"Error getting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve conversation")


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
    return {"status": "healthy", "service": "chat-api"}