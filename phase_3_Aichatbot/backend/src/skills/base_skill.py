"""
Base skill class for the AI Agent Platform
All skills should inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel


class SkillResult(BaseModel):
    """Standard result format for all skills"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class BaseSkill(ABC):
    """Abstract base class for all skills in the system"""

    @abstractmethod
    def get_skill_name(self) -> str:
        """
        Return the name of the skill

        Returns:
            str: The skill name identifier
        """
        pass

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute the skill with the given parameters

        Args:
            params: Parameters required for skill execution

        Returns:
            SkillResult: Result of the skill execution
        """
        pass

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        Validate the parameters before execution

        Args:
            params: Parameters to validate

        Returns:
            bool: True if parameters are valid, False otherwise
        """
        # Default implementation - subclasses can override
        return True

    def get_required_params(self) -> list:
        """
        Get the list of required parameters for this skill

        Returns:
            list: List of required parameter names
        """
        # Default implementation - subclasses can override
        return []

    def get_optional_params(self) -> list:
        """
        Get the list of optional parameters for this skill

        Returns:
            list: List of optional parameter names
        """
        # Default implementation - subclasses can override
        return []