"""
Basic logging setup for the AI Agent Platform
Implements FR-011: System MUST implement basic logging for requests and errors for debugging and monitoring
"""
import logging
import sys
from datetime import datetime
from typing import Dict, Any
from functools import wraps
from ..db.settings import settings


# Create a custom logger
logger = logging.getLogger("ai_agent_platform")
logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)

# Create formatters and add it to handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)
console_handler.setFormatter(formatter)

# Add handlers to the logger
if not logger.handlers:
    logger.addHandler(console_handler)

# Prevent propagation to root logger to avoid duplicate logs
logger.propagate = False


def log_request(user_id: str, endpoint: str, method: str = "POST"):
    """
    Log incoming requests

    Args:
        user_id: ID of the user making the request
        endpoint: API endpoint being accessed
        method: HTTP method (default: POST)
    """
    logger.info(f"Request - User: {user_id}, Method: {method}, Endpoint: {endpoint}")


def log_error(error: Exception, context: str = ""):
    """
    Log errors with context

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_provider_call(provider: str, model: str, tokens_used: int = 0):
    """
    Log calls to LLM providers

    Args:
        provider: Name of the LLM provider (e.g., 'gemini', 'openai')
        model: Model used for the call
        tokens_used: Number of tokens consumed (if available)
    """
    logger.info(f"Provider call - Provider: {provider}, Model: {model}, Tokens: {tokens_used}")


def log_skill_execution(skill_name: str, duration: float, success: bool = True, user_id: str = None):
    """
    Log skill execution

    Args:
        skill_name: Name of the skill executed
        duration: Time taken to execute the skill (in seconds)
        success: Whether the skill execution was successful
        user_id: ID of the user triggering the skill (optional)
    """
    user_info = f"User: {user_id}, " if user_id else ""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Skill execution - {user_info}Skill: {skill_name}, Duration: {duration:.2f}s, Status: {status}")


def log_agent_decision(agent_type: str, decision: str, confidence: float = None):
    """
    Log agent decisions

    Args:
        agent_type: Type of agent making the decision
        decision: Description of the decision made
        confidence: Confidence level of the decision (optional)
    """
    conf_str = f", Confidence: {confidence}" if confidence else ""
    logger.info(f"Agent decision - Type: {agent_type}, Decision: {decision}{conf_str}")


def log_function_call(func):
    """
    Decorator to log function calls

    Args:
        func: The function to wrap
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling function: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} raised an exception: {str(e)}", exc_info=True)
            raise
    return wrapper


class Logger:
    """Utility class for centralized logging operations"""

    @staticmethod
    def info(message: str, extra: Dict[str, Any] = None):
        """Log an info message"""
        if extra:
            logger.info(f"{message} - Extra: {extra}")
        else:
            logger.info(message)

    @staticmethod
    def warning(message: str, extra: Dict[str, Any] = None):
        """Log a warning message"""
        if extra:
            logger.warning(f"{message} - Extra: {extra}")
        else:
            logger.warning(message)

    @staticmethod
    def error(message: str, extra: Dict[str, Any] = None, exc_info: bool = False):
        """Log an error message"""
        if extra:
            logger.error(f"{message} - Extra: {extra}", exc_info=exc_info)
        else:
            logger.error(message, exc_info=exc_info)

    @staticmethod
    def debug(message: str, extra: Dict[str, Any] = None):
        """Log a debug message"""
        if extra:
            logger.debug(f"{message} - Extra: {extra}")
        else:
            logger.debug(message)


# Initialize logging configuration
def setup_logging():
    """
    Setup logging configuration based on settings
    """
    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    # Add file handler if in production mode
    if not settings.debug:
        from logging.handlers import RotatingFileHandler

        # Create logs directory if it doesn't exist
        import os
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(
            f"{log_dir}/ai_agent_platform.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


# Setup logging when module is imported
setup_logging()