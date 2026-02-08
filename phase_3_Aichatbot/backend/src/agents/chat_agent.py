"""
Conversational agent for the AI Agent Platform
Handles general conversation and chat interactions
"""
from typing import Dict, Any, Optional
from ..models.message import MessageCreate
from ..services.conversation_service import ConversationService
from .base_agent import BaseAgent, AgentResponse
from ..providers.base_provider import BaseProvider, Message as ProviderMessage
from ..utils.logging import log_provider_call, Logger
from ..db.settings import settings
import asyncio


class ChatAgent(BaseAgent):
    """
    The conversational agent is responsible for:
    1. Handling general conversation requests
    2. Managing the conversation flow
    3. Generating appropriate responses using LLM providers
    4. Maintaining context across conversation turns
    """

    def __init__(self, conversation_service: ConversationService, provider: BaseProvider):
        super().__init__(conversation_service)

        # Provider for LLM interactions
        self.provider = provider

        # Validate provider configuration
        if not self.provider.validate_config():
            raise ValueError("Invalid provider configuration")

    def get_agent_type(self) -> str:
        """Return the type of agent"""
        return "chat"

    async def process(self, message: str, conversation_id: str, user_id: str) -> AgentResponse:
        """
        Process a user message and generate a conversational response

        Args:
            message: The user's input message
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            AgentResponse: The agent's response with metadata
        """
        try:
            # Log the incoming request
            Logger.info(f"Chat agent processing message: {message[:50]}...",
                       extra={"conversation_id": conversation_id, "user_id": user_id})

            # Add the user's message to the conversation
            user_message = MessageCreate(role="user", content=message, user_id=user_id)
            await self.conversation_service.add_message_to_conversation(conversation_id, user_message)

            # Retrieve conversation history to maintain context
            conversation_history = await self.conversation_service.get_conversation_history(conversation_id)

            # Convert conversation history to provider messages
            # Ensure we maintain the correct chronological order
            provider_messages = []
            for msg in conversation_history:
                provider_messages.append(ProviderMessage(
                    role=msg.role,
                    content=msg.content
                ))

            # Generate response from the provider
            provider_response = await self.provider.generate_response(
                messages=provider_messages,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )

            if provider_response.error:
                Logger.error(f"Provider error: {provider_response.error}")
                return AgentResponse(
                    content=f"I'm experiencing difficulties connecting to the AI service. Error: {provider_response.error}",
                    error=provider_response.error,
                    metadata={"provider_error": True}
                )

            # Add the assistant's response to the conversation
            assistant_message = MessageCreate(
                role="assistant",
                content=provider_response.content,
                user_id=user_id,  # Include user_id for assistant messages too
                tool_calls=provider_response.tool_calls
            )
            await self.conversation_service.add_message_to_conversation(conversation_id, assistant_message)

            # Log the provider call
            log_provider_call(
                provider=settings.llm_provider,
                model=self.provider.model_name or "default",
                tokens_used=len(provider_response.content.split())  # Rough token estimation
            )

            # Return the response
            return AgentResponse(
                content=provider_response.content,
                metadata={
                    "agent_type": self.get_agent_type(),
                    "provider_used": settings.LLM_PROVIDER,
                    "model_used": self.provider.model_name or "default",
                    "tool_calls": provider_response.tool_calls,
                    "conversation_id": conversation_id
                },
                tool_calls=provider_response.tool_calls
            )

        except Exception as e:
            Logger.error(f"Error in chat agent: {str(e)}", extra={"user_id": user_id, "conversation_id": conversation_id})

            return AgentResponse(
                content="I'm sorry, I encountered an error while processing your request. Please try again.",
                error=str(e),
                metadata={"error_occurred": True}
            )

    async def get_conversation_context(self, conversation_id: str, max_history: int = 10) -> list:
        """
        Retrieve conversation context for maintaining continuity

        Args:
            conversation_id: ID of the conversation
            max_history: Maximum number of messages to retrieve

        Returns:
            list: List of messages in the conversation
        """
        try:
            # Get conversation history (limiting to max_history)
            conversation_history = await self.conversation_service.get_conversation_history(
                conversation_id, limit=max_history
            )

            # Convert to the format expected by the provider
            context_messages = []
            for msg in conversation_history:
                context_messages.append({
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
                })

            return context_messages
        except Exception as e:
            Logger.error(f"Error retrieving conversation context: {str(e)}")
            return []

    async def validate_input(self, message: str) -> tuple[bool, str]:
        """
        Validate the user input before processing

        Args:
            message: The user's input message

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not message or len(message.strip()) == 0:
            return False, "Message cannot be empty"

        if len(message) > 10000:  # Arbitrary limit, can be configured
            return False, "Message is too long"

        return True, ""