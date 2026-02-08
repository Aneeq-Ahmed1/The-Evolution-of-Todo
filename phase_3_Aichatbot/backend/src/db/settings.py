"""
Settings configuration for database connection
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    # Force PostgreSQL connection - no SQLite fallback allowed in production
    database_url: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate that DATABASE_URL is set and is a PostgreSQL URL
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required and must be set to a PostgreSQL URL")

        if not (self.database_url.startswith("postgresql://") or
                self.database_url.startswith("postgresql+psycopg://")):
            raise ValueError(f"DATABASE_URL must be a PostgreSQL URL. Got: {self.database_url}")

    # Authentication settings
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # LLM Provider settings
    llm_provider: str = os.getenv("LLM_PROVIDER", "gemini")  # gemini, openai, anthropic
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4")  # or gemini-pro depending on provider

    # Rate limiting settings
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # in seconds

    # Token efficiency settings
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Data retention settings
    conversation_retention_days: int = int(os.getenv("CONVERSATION_RETENTION_DAYS", "30"))

    # Environment settings
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    class Config:
        # Look for .env file in the same directory as this file
        env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = False  # Allow both cases


settings = Settings()