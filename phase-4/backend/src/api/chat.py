from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from sqlmodel import Session, select
from ..database.session import get_session
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.chat_task import ChatTask
from pydantic import BaseModel
from ..agents.todo_agent import TodoAgent


# Create a dictionary to store agents per user to maintain user-specific state
# This ensures that each user has their own agent instance with their own display_index -> task_id mapping
_user_agents: Dict[str, TodoAgent] = {}


def get_or_create_agent(user_id: str, session: Session) -> TodoAgent:
    """
    Get or create a TodoAgent instance for a specific user.
    Each user gets their own agent instance to maintain their display_index -> task_id mapping.
    The session is passed to the agent methods as needed for database operations.
    """
    if user_id not in _user_agents:
        _user_agents[user_id] = TodoAgent(session)

    # Update the session for this operation (important for database operations)
    agent = _user_agents[user_id]
    agent.session = session
    return agent


def cleanup_agent(user_id: str):
    """
    Remove an agent when a user logs out or session ends.
    This helps prevent memory leaks by cleaning up unused agent instances.
    """
    if user_id in _user_agents:
        del _user_agents[user_id]


router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: int = None  # Optional: integer
    message: str  # Required: string


class ChatResponse(BaseModel):
    conversation_id: int  # Integer
    response: str  # String
    tool_calls: list  # Array of tool calls executed


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest, session: Session = Depends(get_session)):
    """
    Process user message and return AI response.
    """
    # Validate request
    if not request.message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required"
        )

    # Get or create conversation
    conversation = None
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Store user message
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()

    # Process message with user-specific AI agent
    agent = get_or_create_agent(user_id, session)
    ai_response = agent.process_message(user_id, request.message)

    # Store AI response
    ai_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=ai_response
    )
    session.add(ai_message)
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=ai_response,
        tool_calls=[]  # In a real implementation, this would contain the actual tool calls made
    )