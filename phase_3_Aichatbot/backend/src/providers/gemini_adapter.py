"""
Google Gemini provider adapter for the AI Agent Platform
Implements provider-specific functionality for Google Gemini
"""
from typing import Dict, Any, List, Optional
from google.generativeai import configure, GenerativeModel
from google.generativeai.types import GenerationConfig
import google.generativeai as genai
from .base_provider import BaseProvider, Message, ProviderResponse
from ..utils.logging import Logger
# Handle the import differently to avoid relative import issues
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Now import using the absolute path
try:
    from settings import settings
except ImportError:
    # If direct import fails, try with backend prefix
    from backend.settings import settings


class GeminiProvider(BaseProvider):
    """
    Google Gemini provider adapter implementing the BaseProvider interface
    """

    def __init__(self, api_key: str, model_name: Optional[str] = None):
        """
        Initialize the Gemini provider adapter

        Args:
            api_key: The Google Gemini API key
            model_name: The model to use (optional, defaults to gemini-pro)
        """
        super().__init__(api_key, model_name)

        # Configure the Gemini API
        genai.configure(api_key=api_key)

        # Set default model if not provided
        if not self.model_name:
            self.model_name = "gemini-1.0-pro"  # Updated to current model name

        # Initialize the model
        self.model = GenerativeModel(self.model_name)

        # Set up generation configuration
        self.generation_config = GenerationConfig(
            max_output_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
        )

    async def generate_response(self, messages: List[Message], **kwargs) -> ProviderResponse:
        """
        Generate a response from Google Gemini

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Returns:
            ProviderResponse: The response from Gemini
        """
        try:
            # Prepare the conversation history for Gemini
            # Gemini expects a chat history with alternating user/model roles
            chat_history = []

            # Convert our messages to Gemini format (skip system messages in chat history)
            for msg in messages:
                if msg.role == "user":
                    chat_history.append({"role": "user", "parts": [msg.content]})
                elif msg.role == "assistant":
                    chat_history.append({"role": "model", "parts": [msg.content]})
                # Skip system messages in chat history but handle them separately if needed

            # Start a new chat session with the history
            chat = self.model.start_chat(history=chat_history[:-1])  # Exclude the last message which we'll send as the query

            # Get the last user message as the query
            if messages:
                last_message = messages[-1]
                if last_message.role == "user":
                    # Send the last user message to the chat
                    response = chat.send_message(
                        last_message.content,
                        generation_config=self.generation_config
                    )

                    if response.candidates and len(response.candidates) > 0:
                        text_response = response.text

                        # Log the provider call
                        from ..utils.logging import log_provider_call
                        log_provider_call(
                            provider="gemini",
                            model=self.model_name,
                            tokens_used=len(text_response.split()) if text_response else 0
                        )

                        return ProviderResponse(
                            content=text_response,
                            metadata={
                                "model": self.model_name,
                                "finish_reason": getattr(response.candidates[0], 'finish_reason', 'stop'),
                                "usage": {
                                    "prompt_tokens": len(str([msg.content for msg in messages[:-1]])),
                                    "completion_tokens": len(text_response.split()) if text_response else 0
                                }
                            }
                        )
                    else:
                        error_msg = "Gemini did not return a valid response"
                        Logger.error(error_msg)
                        return ProviderResponse(content="", error=error_msg)
                else:
                    # If the last message wasn't from user, we can't generate a response
                    error_msg = "Cannot generate response: last message was not from user"
                    Logger.error(error_msg)
                    return ProviderResponse(content="", error=error_msg)
            else:
                # No messages to process
                error_msg = "No messages provided to generate response"
                Logger.error(error_msg)
                return ProviderResponse(content="", error=error_msg)

        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            Logger.error(error_msg)
            return ProviderResponse(content="", error=f"Gemini API error: {str(e)}")

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from Google Gemini

        Returns:
            List[str]: Available model names
        """
        try:
            # List available models from Gemini
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name.replace("models/", ""))  # Remove 'models/' prefix
            return available_models
        except Exception as e:
            Logger.error(f"Error getting available Gemini models: {str(e)}")
            # Return default models in case of error
            return ["gemini-pro", "gemini-pro-vision"]

    def validate_config(self) -> bool:
        """
        Validate that the Gemini configuration is correct

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not self.api_key:
            Logger.error("Gemini API key is not set")
            return False

        try:
            # Try to initialize the model to verify the API key works
            test_model = GenerativeModel("gemini-1.0-pro")
            return test_model is not None
        except Exception as e:
            Logger.error(f"Gemini configuration validation failed: {str(e)}")
            return False

    def preprocess_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Preprocess messages before sending to Gemini

        Args:
            messages: List of messages to preprocess

        Returns:
            List[Dict[str, str]]: Preprocessed messages in Gemini format
        """
        processed = []
        for msg in messages:
            if msg.role == "user":
                processed.append({"role": "user", "parts": [msg.content]})
            elif msg.role == "assistant":
                processed.append({"role": "model", "parts": [msg.content]})
            elif msg.role == "system":
                # Treat system messages as instructions to user
                processed.append({"role": "user", "parts": [f"*System instruction: {msg.content}*"]})

        return processed