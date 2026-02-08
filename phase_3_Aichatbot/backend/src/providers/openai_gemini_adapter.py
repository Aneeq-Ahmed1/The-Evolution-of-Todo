"""
OpenAI-compatible Gemini provider adapter for the AI Agent Platform
Implements OpenAI SDK interface while routing inference through Google Gemini
"""
from typing import Dict, Any, List, Optional
from openai import OpenAI
from google.generativeai import configure, GenerativeModel
import google.generativeai as genai
from .base_provider import BaseProvider, Message, ProviderResponse
from ..utils.logging import Logger
from ..db.settings import settings
import asyncio
import json


class OpenAIGeminiProvider(BaseProvider):
    """
    OpenAI-compatible provider adapter that routes requests through Google Gemini
    Implements OpenAI SDK interface while using Gemini as the underlying model
    """

    def __init__(self, api_key: str, model_name: Optional[str] = None):
        """
        Initialize the OpenAI-compatible Gemini provider adapter

        Args:
            api_key: The Google Gemini API key (used for Gemini, not OpenAI)
            model_name: The Gemini model to use (optional, defaults to gemini-pro)
        """
        super().__init__(api_key, model_name)

        # Set default model if not provided
        if not self.model_name:
            self.model_name = "gemini-pro"

        # Configure the Gemini API (this is what will actually process the request)
        genai.configure(api_key=api_key)

        # Initialize the Gemini model that will process requests
        self.gemini_model = GenerativeModel(self.model_name)

        # Create a fake OpenAI client for compatibility (not actually used for requests)
        # We'll intercept calls and route them to Gemini
        self.fake_client = OpenAI(api_key="fake-key-for-compatibility")

    async def generate_response(self, messages: List[Message], **kwargs) -> ProviderResponse:
        """
        Generate a response by routing through Gemini but using OpenAI-compatible format

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Returns:
            ProviderResponse: The response from Gemini formatted as OpenAI response
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
                # System messages are handled differently in Gemini

            # If there are system messages, we'll incorporate them into the first user message
            system_instructions = []
            user_messages = []

            for msg in messages:
                if msg.role == "system":
                    system_instructions.append(msg.content)
                elif msg.role == "user":
                    user_messages.append(msg.content)

            # Start a new chat session with the history
            chat = self.gemini_model.start_chat(history=chat_history[:-1])  # Exclude the last message which we'll send as the query

            # Get the last user message as the query
            if messages:
                last_message = messages[-1]
                if last_message.role == "user":
                    # If we have system instructions, prepend them to the last message
                    final_query = last_message.content
                    if system_instructions:
                        system_prompt = "\n".join(system_instructions)
                        final_query = f"{system_prompt}\n\n{final_query}"

                    # Send the final query to Gemini
                    response = chat.send_message(
                        final_query,
                        generation_config={
                            "max_output_tokens": kwargs.get("max_tokens", settings.max_tokens),
                            "temperature": kwargs.get("temperature", settings.temperature),
                        }
                    )

                    if response.candidates and len(response.candidates) > 0:
                        text_response = response.text

                        # Log the provider call
                        from ..utils.logging import log_provider_call
                        log_provider_call(
                            provider="gemini-via-openai-interface",
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
                                    "completion_tokens": len(text_response.split()) if text_response else 0,
                                    "total_tokens": len(str([msg.content for msg in messages[:-1]])) + len(text_response.split()) if text_response else 0
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
            error_msg = f"OpenAI-Gemini adapter error: {str(e)}"
            Logger.error(error_msg)
            return ProviderResponse(content="", error=f"OpenAI-Gemini adapter error: {str(e)}")

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
            return ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]

    def validate_config(self) -> bool:
        """
        Validate that the OpenAI-Gemini configuration is correct

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not self.api_key:
            Logger.error("Gemini API key is not set for OpenAI-Gemini adapter")
            return False

        try:
            # Try to initialize the model to verify the API key works
            test_model = GenerativeModel("gemini-pro")
            # Try a simple generation to validate
            response = test_model.generate_content("Hello", generation_config={"max_output_tokens": 10})
            return response is not None and len(response.text) > 0
        except Exception as e:
            Logger.error(f"OpenAI-Gemini configuration validation failed: {str(e)}")
            return False

    def preprocess_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Preprocess messages before sending to OpenAI-compatible interface

        Args:
            messages: List of messages to preprocess

        Returns:
            List[Dict[str, str]]: Preprocessed messages
        """
        processed = []
        for msg in messages:
            processed.append({
                "role": msg.role,
                "content": msg.content
            })

        return processed