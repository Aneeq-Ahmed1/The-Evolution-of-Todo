"""
Base provider adapter class for the AI Agent Platform
All provider adapters should inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """Represents a message in the conversation"""
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: str


class ProviderResponse(BaseModel):
    """Standard response format from any provider"""
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    metadata: Dict[str, Any] = {}
    error: Optional[str] = None


class BaseProvider(ABC):
    """Abstract base class for all LLM providers"""

    def __init__(self, api_key: str, model_name: Optional[str] = None):
        """
        Initialize the provider adapter

        Args:
            api_key: The API key for the provider
            model_name: The model to use (optional, defaults to provider's default)
        """
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    async def generate_response(self, messages: List[Message], **kwargs) -> ProviderResponse:
        """
        Generate a response from the provider

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Returns:
            ProviderResponse: The response from the provider
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from this provider

        Returns:
            List[str]: Available model names
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate that the provider configuration is correct

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        pass

    def get_max_tokens_limit(self) -> int:
        """
        Get the maximum number of tokens allowed by this provider

        Returns:
            int: Maximum token limit
        """
        # Default implementation - providers can override
        return 4096

    def preprocess_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Preprocess messages before sending to provider

        Args:
            messages: List of messages to preprocess

        Returns:
            List[Dict[str, str]]: Preprocessed messages
        """
        # Default preprocessing - convert to the format expected by most providers
        processed = []
        for msg in messages:
            processed.append({
                "role": msg.role,
                "content": msg.content
            })
        return processed