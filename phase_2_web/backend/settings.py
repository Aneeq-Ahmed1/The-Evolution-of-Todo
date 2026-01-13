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

    # Optional settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    class Config:
        # Look for .env file in the same directory as this file
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        case_sensitive = False  # Allow both cases


# Create a single instance of settings
settings = Settings()