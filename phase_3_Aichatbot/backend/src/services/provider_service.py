"""
Provider service for the AI Agent Platform
Implements the provider factory/service to select provider based on configuration
Implements FR-001: System MUST provide a standardized interface that routes requests to configurable LLM providers
Implements FR-007: System MUST handle provider switching with minimal configuration changes
"""
from typing import Dict, Any, List, Optional
from ..providers.base_provider import BaseProvider
from ..providers.gemini_adapter import GeminiProvider
from ..providers.openai_adapter import OpenAIProvider
from ..db.settings import settings
from ..utils.logging import Logger
import importlib


class ProviderService:
    """
    Service class to manage and select LLM providers based on configuration
    """

    def __init__(self):
        """
        Initialize the provider service
        """
        self.providers = {}
        self.active_provider = None
        self._initialize_providers()

    def _initialize_providers(self):
        """
        Initialize all available providers based on configuration
        """
        # Initialize providers based on available API keys
        if settings.GEMINI_API_KEY:
            try:
                # Use OpenAI-compatible adapter that routes through Gemini
                from ..providers.openai_gemini_adapter import OpenAIGeminiProvider
                gemini_provider = OpenAIGeminiProvider(
                    api_key=settings.GEMINI_API_KEY,
                    model_name=getattr(settings, 'gemini_model_name', None)
                )
                if gemini_provider.validate_config():
                    self.providers['gemini'] = gemini_provider
                    Logger.info("OpenAI-Gemini provider initialized and validated")
                else:
                    Logger.warning("OpenAI-Gemini provider configuration is invalid")
            except Exception as e:
                Logger.error(f"Failed to initialize OpenAI-Gemini provider: {str(e)}")

        if settings.OPENAI_API_KEY:
            try:
                openai_provider = OpenAIProvider(
                    api_key=settings.OPENAI_API_KEY,
                    model_name=getattr(settings, 'openai_model_name', None)
                )
                if openai_provider.validate_config():
                    self.providers['openai'] = openai_provider
                    Logger.info("OpenAI provider initialized and validated")
                else:
                    Logger.warning("OpenAI provider configuration is invalid")
            except Exception as e:
                Logger.error(f"Failed to initialize OpenAI provider: {str(e)}")

        # Add support for other providers as needed
        if settings.ANTHROPIC_API_KEY:
            try:
                # Dynamically import Anthropic provider if available
                from ..providers.anthropic_adapter import AnthropicProvider
                anthropic_provider = AnthropicProvider(
                    api_key=settings.ANTHROPIC_API_KEY,
                    model_name=getattr(settings, 'anthropic_model_name', None)
                )
                if anthropic_provider.validate_config():
                    self.providers['anthropic'] = anthropic_provider
                    Logger.info("Anthropic provider initialized and validated")
                else:
                    Logger.warning("Anthropic provider configuration is invalid")
            except ImportError:
                Logger.info("Anthropic provider not available")
            except Exception as e:
                Logger.error(f"Failed to initialize Anthropic provider: {str(e)}")

        # Set the active provider based on configuration
        self._set_active_provider(settings.LLM_PROVIDER)

    def _set_active_provider(self, provider_name: str):
        """
        Set the active provider based on the configuration

        Args:
            provider_name: Name of the provider to activate
        """
        if provider_name in self.providers:
            self.active_provider = self.providers[provider_name]
            Logger.info(f"Active provider set to: {provider_name}")
        else:
            # If the configured provider is not available, use the first available one
            if self.providers:
                first_provider_name = next(iter(self.providers))
                self.active_provider = self.providers[first_provider_name]
                Logger.warning(f"Configured provider '{provider_name}' not available. Using '{first_provider_name}' instead.")
            else:
                Logger.error("No providers are available. Check your configuration.")
                raise ValueError("No valid providers available")

    def get_provider(self, provider_name: Optional[str] = None) -> BaseProvider:
        """
        Get a specific provider or the active provider

        Args:
            provider_name: Optional name of the provider to get (defaults to active provider)

        Returns:
            BaseProvider: The requested provider
        """
        if provider_name:
            if provider_name in self.providers:
                return self.providers[provider_name]
            else:
                Logger.warning(f"Provider '{provider_name}' not available, returning active provider")
                return self.active_provider
        else:
            return self.active_provider

    def get_active_provider(self) -> BaseProvider:
        """
        Get the currently active provider

        Returns:
            BaseProvider: The active provider
        """
        return self.active_provider

    def get_available_providers(self) -> List[str]:
        """
        Get a list of available providers

        Returns:
            List[str]: Names of available providers
        """
        return list(self.providers.keys())

    def switch_provider(self, provider_name: str) -> bool:
        """
        Switch the active provider

        Args:
            provider_name: Name of the provider to switch to

        Returns:
            bool: True if switch was successful, False otherwise
        """
        if provider_name in self.providers:
            self.active_provider = self.providers[provider_name]
            Logger.info(f"Switched active provider to: {provider_name}")
            return True
        else:
            Logger.error(f"Cannot switch to provider '{provider_name}': not available")
            return False

    def validate_provider_config(self, provider_name: str) -> bool:
        """
        Validate the configuration of a specific provider

        Args:
            provider_name: Name of the provider to validate

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if provider_name in self.providers:
            return self.providers[provider_name].validate_config()
        else:
            Logger.error(f"Provider '{provider_name}' not available for validation")
            return False

    def get_provider_models(self, provider_name: str) -> List[str]:
        """
        Get available models for a specific provider

        Args:
            provider_name: Name of the provider

        Returns:
            List[str]: Available models for the provider
        """
        if provider_name in self.providers:
            return self.providers[provider_name].get_available_models()
        else:
            Logger.error(f"Provider '{provider_name}' not available")
            return []

    def is_provider_available(self, provider_name: str) -> bool:
        """
        Check if a provider is available

        Args:
            provider_name: Name of the provider to check

        Returns:
            bool: True if provider is available, False otherwise
        """
        return provider_name in self.providers

    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about all available providers

        Returns:
            Dict[str, Any]: Information about available providers
        """
        info = {
            "active_provider": self.active_provider.__class__.__name__.replace("Provider", "").lower() if self.active_provider else None,
            "available_providers": list(self.providers.keys()),
            "provider_details": {}
        }

        for name, provider in self.providers.items():
            info["provider_details"][name] = {
                "name": provider.__class__.__name__,
                "model": provider.model_name,
                "validated": provider.validate_config()
            }

        return info

    async def generate_response(self, messages: List, **kwargs) -> Any:
        """
        Generate a response using the active provider

        Args:
            messages: List of messages for the conversation
            **kwargs: Additional parameters for generation

        Returns:
            Any: Response from the active provider
        """
        if not self.active_provider:
            raise ValueError("No active provider available")

        # Convert messages to the format expected by the base provider
        from ..providers.base_provider import Message as ProviderMessage
        provider_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                provider_messages.append(ProviderMessage(
                    role=msg.get("role", "user"),
                    content=msg.get("content", "")
                ))
            else:
                # Assume it's already in the right format
                provider_messages.append(msg)

        return await self.active_provider.generate_response(provider_messages, **kwargs)


# Global provider service instance
provider_service = ProviderService()


def get_provider_service() -> ProviderService:
    """
    Get the global provider service instance

    Returns:
        ProviderService: The global provider service instance
    """
    return provider_service