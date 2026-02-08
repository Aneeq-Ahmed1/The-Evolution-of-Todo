from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    DATABASE_URL: str

    # Authentication settings
    BETTER_AUTH_SECRET: str

    # JWT settings
    SECRET_KEY: str = "your-super-secret-key-change-in-production"  # Default for development
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    conversation_retention_days: int = 30  # Default retention period

    # LLM Provider settings
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    MODEL_NAME: str = "gpt-4"  # or gemini-pro depending on provider

    # Rate limiting settings
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # in seconds

    # Token efficiency settings
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7

    # Optional settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    class Config:
        # Look for .env file in the same directory as this file
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        case_sensitive = False  # Allow both cases


# Create a single instance of settings
settings = Settings()