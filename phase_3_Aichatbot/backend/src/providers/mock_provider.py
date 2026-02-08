"""
Mock provider for testing when no LLM API key is configured
"""
from typing import Dict, Any, List, Optional
from ..providers.base_provider import BaseProvider, Message, ProviderResponse
from ..utils.logging import Logger


class MockProvider(BaseProvider):
    """
    A mock provider that simulates LLM responses for testing purposes
    when no actual LLM API key is configured.
    """

    def __init__(self, api_key: str = None, model_name: Optional[str] = "mock-model"):
        """
        Initialize the mock provider
        
        Args:
            api_key: Not used for mock provider
            model_name: Name of the mock model
        """
        super().__init__(api_key or "mock-key", model_name)

    async def generate_response(self, messages: List[Message], **kwargs) -> ProviderResponse:
        """
        Generate a mock response
        
        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Returns:
            ProviderResponse: Mock response
        """
        try:
            # Get the last user message to formulate a response
            last_user_message = None
            for msg in reversed(messages):
                if msg.role == "user":
                    last_user_message = msg.content
                    break

            if last_user_message:
                # Generate a contextual response based on the user's message
                if any(word in last_user_message.lower() for word in ["hello", "hi", "hey", "greet"]):
                    response_text = "Hello! I'm your AI assistant. How can I help you today?"
                elif any(word in last_user_message.lower() for word in ["help", "what can you do"]):
                    response_text = "I can help you manage tasks, answer questions, and more! Try asking me to add, list, or complete tasks."
                elif any(word in last_user_message.lower() for word in ["task", "todo", "add"]):
                    response_text = "Sure! You can add tasks by saying something like 'Add a task: Buy groceries'. I'll help you manage your tasks."
                elif any(word in last_user_message.lower() for word in ["list", "show", "view"]):
                    response_text = "You can view your tasks by saying 'Show my tasks'. I'll list all your tasks for you."
                else:
                    response_text = f"I received your message: '{last_user_message}'. I'm a task management assistant. You can ask me to add, list, complete, or delete tasks."
            else:
                response_text = "Hello! I'm your AI assistant. How can I help you today?"

            Logger.info(f"Mock provider returning response: {response_text[:50]}...")

            return ProviderResponse(
                content=response_text,
                metadata={
                    "model": self.model_name or "mock-model",
                    "provider": "mock",
                    "usage": {
                        "prompt_tokens": len(last_user_message.split()) if last_user_message else 0,
                        "completion_tokens": len(response_text.split()),
                        "total_tokens": len(last_user_message.split()) + len(response_text.split()) if last_user_message else len(response_text.split())
                    }
                }
            )
        except Exception as e:
            error_msg = f"Mock provider error: {str(e)}"
            Logger.error(error_msg)
            return ProviderResponse(content="Sorry, I encountered an error processing your request.", error=error_msg)

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from the mock provider

        Returns:
            List[str]: Available model names
        """
        return ["mock-model-1", "mock-model-2"]

    def validate_config(self) -> bool:
        """
        Validate that the mock provider configuration is correct

        Returns:
            bool: Always True for mock provider
        """
        return True