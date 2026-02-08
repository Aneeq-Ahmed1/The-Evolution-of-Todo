"""
OpenAI provider adapter for the AI Agent Platform
Implements provider-specific functionality for OpenAI
"""
from typing import Dict, Any, List, Optional
from openai import OpenAI
from .base_provider import BaseProvider, Message, ProviderResponse
from ..utils.logging import Logger
from ..db.settings import settings
import asyncio


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider adapter implementing the BaseProvider interface
    """

    def __init__(self, api_key: str, model_name: Optional[str] = None):
        """
        Initialize the OpenAI provider adapter

        Args:
            api_key: The OpenAI API key
            model_name: The model to use (optional, defaults to gpt-3.5-turbo)
        """
        super().__init__(api_key, model_name)

        # Set default model if not provided
        if not self.model_name:
            self.model_name = "gpt-3.5-turbo"

        # Initialize the OpenAI client
        self.client = OpenAI(api_key=api_key)

    async def generate_response(self, messages: List[Message], **kwargs) -> ProviderResponse:
        """
        Generate a response from OpenAI

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Returns:
            ProviderResponse: The response from OpenAI
        """
        try:
            # Convert our Message objects to the format expected by OpenAI
            openai_messages = []
            for msg in messages:
                openai_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Extract additional parameters that might be passed
            max_tokens = kwargs.get("max_tokens", settings.MAX_TOKENS)
            temperature = kwargs.get("temperature", settings.TEMPERATURE)

            # Call the OpenAI API asynchronously
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model_name,
                    messages=openai_messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **{k: v for k, v in kwargs.items() if k not in ['max_tokens', 'temperature']}
                )
            )

            # Extract the response
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                finish_reason = response.choices[0].finish_reason

                # Check if there are tool calls
                tool_calls = None
                if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                    tool_calls = []
                    for tool_call in response.choices[0].message.tool_calls:
                        tool_calls.append({
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        })

                # Log the provider call
                from ..utils.logging import log_provider_call
                log_provider_call(
                    provider="openai",
                    model=self.model_name,
                    tokens_used=response.usage.total_tokens if hasattr(response, 'usage') and response.usage else len(content.split()) if content else 0
                )

                return ProviderResponse(
                    content=content or "",
                    tool_calls=tool_calls,
                    metadata={
                        "model": self.model_name,
                        "finish_reason": finish_reason,
                        "usage": {
                            "prompt_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0,
                            "completion_tokens": response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0,
                            "total_tokens": response.usage.total_tokens if hasattr(response, 'usage') and response.usage else len(content.split()) if content else 0
                        } if hasattr(response, 'usage') and response.usage else {}
                    }
                )
            else:
                error_msg = "OpenAI did not return a valid response"
                Logger.error(error_msg)
                return ProviderResponse(content="", error=error_msg)

        except Exception as e:
            error_msg = f"OpenAI API error: {str(e)}"
            Logger.error(error_msg)
            return ProviderResponse(content="", error=error_msg)

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from OpenAI

        Returns:
            List[str]: Available model names
        """
        try:
            # Fetch available models from OpenAI
            models_list = self.client.models.list()
            available_models = [model.id for model in models_list.data]
            return available_models
        except Exception as e:
            Logger.error(f"Error getting available OpenAI models: {str(e)}")
            # Return a default list in case of error
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

    def validate_config(self) -> bool:
        """
        Validate that the OpenAI configuration is correct

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not self.api_key:
            Logger.error("OpenAI API key is not set")
            return False

        try:
            # Try to make a simple API call to validate the key
            # Using a lightweight model for validation
            validation_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
                temperature=0
            )

            # If we get a response, the configuration is valid
            return validation_response is not None
        except Exception as e:
            Logger.error(f"OpenAI configuration validation failed: {str(e)}")
            return False

    def preprocess_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Preprocess messages before sending to OpenAI

        Args:
            messages: List of messages to preprocess

        Returns:
            List[Dict[str, str]]: Preprocessed messages in OpenAI format
        """
        processed = []
        for msg in messages:
            processed.append({
                "role": msg.role,
                "content": msg.content
            })

        return processed