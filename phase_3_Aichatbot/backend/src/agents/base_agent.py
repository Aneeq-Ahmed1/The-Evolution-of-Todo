"""
Base agent class for the AI Agent Platform
All agents should inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..services.conversation_service import ConversationService
from ..models.message import MessageCreate


class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    content: str
    metadata: Dict[str, Any] = {}
    tool_calls: Optional[list] = None
    error: Optional[str] = None


class BaseAgent(ABC):
    """Abstract base class for all agents in the system"""

    def __init__(self, conversation_service: ConversationService):
        """
        Initialize the agent with a conversation service

        Args:
            conversation_service: Service to handle conversation persistence
        """
        self.conversation_service = conversation_service

    @abstractmethod
    async def process(self, message: str, conversation_id: str, user_id: str) -> AgentResponse:
        """
        Process a user message and return a response

        Args:
            message: The user's input message
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            AgentResponse: The agent's response with metadata
        """
        pass

    @abstractmethod
    def get_agent_type(self) -> str:
        """
        Return the type of agent (used for identification)

        Returns:
            str: The agent type identifier
        """
        pass

    async def log_interaction(self, user_message: str, agent_response: str, metadata: Dict[str, Any] = None):
        """
        Log the interaction for analytics and debugging

        Args:
            user_message: The original user message
            agent_response: The agent's response
            metadata: Additional metadata about the interaction
        """
        # This would typically log to the SkillExecutionLog or a similar mechanism
        # Implementation will depend on the specific logging requirements
        pass