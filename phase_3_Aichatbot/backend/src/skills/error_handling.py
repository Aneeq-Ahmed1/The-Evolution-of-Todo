"""
Error handling skill for the AI Agent Platform
Provides consistent error handling and user-friendly error messages
"""
from typing import Dict, Any
from .base_skill import BaseSkill, SkillResult
from ..utils.logging import Logger, log_error
import traceback
import re


class ErrorHandlingSkill(BaseSkill):
    """
    The error handling skill is responsible for:
    1. Providing consistent error handling across the system
    2. Generating user-friendly error messages
    3. Logging errors appropriately
    4. Handling different types of errors appropriately
    """

    def __init__(self):
        # Define error categories and their user-friendly messages
        self.error_categories = {
            "authentication": {
                "patterns": [
                    r"auth", r"token", r"credential", r"permission", r"unauthorized", r"forbidden"
                ],
                "message": "There was an authentication issue. Please check your login status and try again."
            },
            "connection": {
                "patterns": [
                    r"connection", r"timeout", r"network", r"offline", r"unreachable", r"socket"
                ],
                "message": "There was a connection issue. Please check your internet connection and try again."
            },
            "provider": {
                "patterns": [
                    r"api", r"rate limit", r"quota", r"exceeded", r"invalid key", r"api key"
                ],
                "message": "The AI service is temporarily unavailable. Please try again later."
            },
            "validation": {
                "patterns": [
                    r"validation", r"invalid", r"value error", r"type error"
                ],
                "message": "The input provided is not valid. Please check and try again."
            },
            "database": {
                "patterns": [
                    r"database", r"sql", r"constraint", r"duplicate", r"integrity"
                ],
                "message": "There was an issue with the data storage. Please try again."
            },
            "general": {
                "patterns": [],
                "message": "An unexpected error occurred. Our team has been notified."
            }
        }

        # Define sensitive information patterns to mask
        self.sensitive_patterns = [
            r"[A-Z0-9]{32,}",  # Long hex strings (likely tokens/keys)
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card numbers
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Emails (in some contexts)
            r"(password|token|key|secret)\s*[=:]\s*['\"]?(\w+)['\"]?",  # Key-value pairs with sensitive data
        ]

    def get_skill_name(self) -> str:
        """Return the name of the skill"""
        return "error_handling"

    def get_required_params(self) -> list:
        """Get the list of required parameters for this skill"""
        return ["error"]

    def get_optional_params(self) -> list:
        """Get the list of optional parameters for this skill"""
        return ["context", "user_facing", "include_traceback"]

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute the error handling

        Args:
            params: Parameters for the skill execution, must include 'error', optionally 'context', 'user_facing', 'include_traceback'

        Returns:
            SkillResult: Result of the error handling
        """
        try:
            # Validate parameters
            if "error" not in params:
                return SkillResult(
                    success=False,
                    error="Missing 'error' parameter"
                )

            error_input = params["error"]
            context = params.get("context", "")
            user_facing = params.get("user_facing", True)
            include_traceback = params.get("include_traceback", False)

            # Handle different types of error inputs
            if isinstance(error_input, Exception):
                error_msg = str(error_input)
                error_type = type(error_input).__name__
            elif isinstance(error_input, str):
                error_msg = error_input
                error_type = "GenericError"
            else:
                error_msg = str(error_input)
                error_type = "UnknownError"

            # Log the error with context
            log_error(Exception(error_msg), context)

            # Categorize the error
            error_category = self._categorize_error(error_msg)

            # Create a safe error message for users
            user_message = self._create_user_message(error_msg, error_category, user_facing)

            # Create a detailed error report for logging/debugging
            error_report = self._create_error_report(error_msg, error_type, context, include_traceback)

            # Prepare result data
            result_data = {
                "user_message": user_message,
                "error_category": error_category,
                "error_type": error_type,
                "error_report": error_report,
                "context": context
            }

            Logger.warning(f"Error handled", extra={
                "category": error_category,
                "type": error_type,
                "context": context
            })

            return SkillResult(
                success=True,
                data=result_data
            )

        except Exception as e:
            Logger.error(f"Critical error in error handling skill: {str(e)}")
            return SkillResult(
                success=False,
                error="An error occurred while handling another error. Please contact support."
            )

    def _categorize_error(self, error_msg: str) -> str:
        """
        Categorize the error based on its message

        Args:
            error_msg: The error message to categorize

        Returns:
            str: The category of the error
        """
        error_msg_lower = error_msg.lower()

        for category, info in self.error_categories.items():
            if category == "general":
                continue  # Skip general category for pattern matching

            for pattern in info["patterns"]:
                if re.search(pattern, error_msg_lower, re.IGNORECASE):
                    return category

        return "general"

    def _create_user_message(self, error_msg: str, error_category: str, user_facing: bool) -> str:
        """
        Create a user-friendly error message

        Args:
            error_msg: The original error message
            error_category: The category of the error
            user_facing: Whether this is for user display

        Returns:
            str: A user-friendly error message
        """
        if not user_facing:
            # Return original error for internal use
            return error_msg

        # Get the user-friendly message for this category
        category_info = self.error_categories.get(error_category, self.error_categories["general"])
        return category_info["message"]

    def _create_error_report(self, error_msg: str, error_type: str, context: str, include_traceback: bool) -> Dict[str, Any]:
        """
        Create a detailed error report for logging

        Args:
            error_msg: The original error message
            error_type: The type of error
            context: Context information
            include_traceback: Whether to include traceback information

        Returns:
            Dict[str, Any]: A detailed error report
        """
        report = {
            "type": error_type,
            "message": self._mask_sensitive_info(error_msg),
            "context": context,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "category": self._categorize_error(error_msg)
        }

        if include_traceback:
            report["traceback"] = traceback.format_exc()

        return report

    def _mask_sensitive_info(self, text: str) -> str:
        """
        Mask sensitive information in the text

        Args:
            text: Text that may contain sensitive information

        Returns:
            str: Text with sensitive information masked
        """
        masked_text = text

        for pattern in self.sensitive_patterns:
            # Replace sensitive information with [REDACTED]
            masked_text = re.sub(pattern, "[REDACTED]", masked_text, flags=re.IGNORECASE)

        return masked_text

    def handle_api_error(self, exception: Exception, context: str = "") -> SkillResult:
        """
        Convenience method for handling API-related errors

        Args:
            exception: The exception that occurred
            context: Context information

        Returns:
            SkillResult: Result of the error handling
        """
        return self.execute({
            "error": exception,
            "context": f"API_ERROR_{context}",
            "user_facing": True,
            "include_traceback": False
        })

    def handle_validation_error(self, field: str, value: Any, expected_type: str) -> SkillResult:
        """
        Convenience method for handling validation errors

        Args:
            field: The field that failed validation
            value: The invalid value
            expected_type: The expected type

        Returns:
            SkillResult: Result of the error handling
        """
        error_msg = f"Validation failed for field '{field}'. Expected {expected_type}, got {type(value).__name__}"
        return self.execute({
            "error": error_msg,
            "context": f"VALIDATION_ERROR_{field}",
            "user_facing": True,
            "include_traceback": False
        })

    def register_error_category(self, name: str, patterns: list, message: str):
        """
        Register a new error category

        Args:
            name: Name of the category
            patterns: List of regex patterns to identify this category
            message: User-friendly message for this category
        """
        self.error_categories[name] = {
            "patterns": patterns,
            "message": message
        }